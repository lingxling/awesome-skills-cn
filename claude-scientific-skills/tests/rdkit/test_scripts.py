"""Tests for the RDKit cheminformatics helpers.

Every SMARTS pattern the skill ships is a claim about chemistry, and a pattern
that silently matches nothing is the failure mode: the filter reports "0 hits"
and looks like it worked. So the catalogue tests compile every pattern and then
prove each library actually matches a molecule containing that group.

Property calculation is checked against values that are true by definition --
benzene has one aromatic ring and no rotatable bonds, aspirin's formula is
C9H8O4 -- rather than against whatever RDKit currently returns.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import pytest

import skill_contract

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "rdkit"
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

pytest.importorskip("rdkit", reason="rdkit skill needs rdkit")

from rdkit import Chem  # noqa: E402

import molecular_properties  # noqa: E402
import similarity_search  # noqa: E402
import substructure_filter  # noqa: E402

CliHelpTests = skill_contract.cli.help_test_case(SKILL_ROOT)

ASPIRIN = "CC(=O)OC1=CC=CC=C1C(=O)O"
CAFFEINE = "CN1C=NC2=C1C(=O)N(C)C(=O)N2C"
BENZENE = "c1ccccc1"
ETHANOL = "CCO"


class PatternLibraryTests(unittest.TestCase):
    def test_every_shipped_smarts_pattern_compiles(self) -> None:
        # Chem.MolFromSmarts returns None rather than raising, so a typo would
        # silently disable the pattern.
        for library, patterns in substructure_filter.PATTERN_LIBRARIES.items():
            for name, smarts in patterns.items():
                with self.subTest(library=library, pattern=name):
                    self.assertIsNotNone(
                        Chem.MolFromSmarts(smarts), f"{name}: {smarts!r}"
                    )

    def test_the_documented_libraries_are_all_present_and_non_empty(self) -> None:
        libraries = substructure_filter.PATTERN_LIBRARIES
        self.assertEqual(
            set(libraries), {"functional-groups", "rings", "pains", "privileged"}
        )
        for name, patterns in libraries.items():
            with self.subTest(library=name):
                self.assertTrue(patterns)

    def test_representative_patterns_match_the_chemistry_they_name(self) -> None:
        cases = [
            ("functional-groups", "carboxylic_acid", "CC(=O)O"),
            ("functional-groups", "alcohol", ETHANOL),
            ("functional-groups", "nitrile", "CC#N"),
            ("rings", "benzene", BENZENE),
            ("rings", "pyridine", "c1ccncc1"),
            ("privileged", "piperidine", "C1CCNCC1"),
            ("pains", "catechol", "Oc1ccccc1O"),
        ]
        for library, name, smiles in cases:
            with self.subTest(pattern=name):
                query = Chem.MolFromSmarts(
                    substructure_filter.PATTERN_LIBRARIES[library][name]
                )
                molecule = Chem.MolFromSmiles(smiles)
                self.assertIsNotNone(molecule, smiles)
                self.assertTrue(
                    molecule.HasSubstructMatch(query), f"{name} did not match {smiles}"
                )

    def test_a_pattern_does_not_match_a_molecule_that_lacks_it(self) -> None:
        benzene = Chem.MolFromSmiles(BENZENE)
        acid = Chem.MolFromSmarts(
            substructure_filter.PATTERN_LIBRARIES["functional-groups"]["carboxylic_acid"]
        )
        self.assertFalse(benzene.HasSubstructMatch(acid))


class QueryTests(unittest.TestCase):
    def test_a_smarts_string_is_compiled(self) -> None:
        self.assertIsNotNone(substructure_filter.create_pattern_query("[OH][C]"))

    def test_a_plain_smiles_string_is_accepted_as_a_fallback(self) -> None:
        # SMARTS first, SMILES second -- so a user can paste either.
        self.assertIsNotNone(substructure_filter.create_pattern_query("c1ccccc1"))

    def test_an_uninterpretable_pattern_is_refused(self) -> None:
        self.assertIsNone(substructure_filter.create_pattern_query("!!not a pattern!!"))


class FilterTests(unittest.TestCase):
    """`filter_molecules` takes (name, compiled query) pairs, not raw strings."""

    def setUp(self) -> None:
        self.molecules = [
            Chem.MolFromSmiles(smiles) for smiles in (ASPIRIN, BENZENE, ETHANOL, CAFFEINE)
        ]
        for molecule, name in zip(
            self.molecules, ("aspirin", "benzene", "ethanol", "caffeine")
        ):
            molecule.SetProp("_Name", name)

    @staticmethod
    def pattern(name: str, smarts: str) -> tuple:
        return (name, substructure_filter.create_pattern_query(smarts))

    def _names(self, molecules) -> set:
        return {molecule.GetProp("_Name") for molecule in molecules}

    def test_an_include_pattern_keeps_only_matching_molecules(self) -> None:
        kept, _ = substructure_filter.filter_molecules(
            self.molecules, include_patterns=[self.pattern("benzene", "c1ccccc1")]
        )
        self.assertEqual(self._names(kept), {"aspirin", "benzene"})

    def test_an_exclude_pattern_removes_matching_molecules(self) -> None:
        kept, _ = substructure_filter.filter_molecules(
            self.molecules, exclude_patterns=[self.pattern("benzene", "c1ccccc1")]
        )
        self.assertEqual(self._names(kept), {"ethanol", "caffeine"})

    def test_exclusion_wins_over_inclusion(self) -> None:
        kept, _ = substructure_filter.filter_molecules(
            self.molecules,
            include_patterns=[self.pattern("benzene", "c1ccccc1")],
            exclude_patterns=[self.pattern("acid", "C(=O)[OH]")],
        )
        self.assertEqual(self._names(kept), {"benzene"})

    def test_no_patterns_keeps_everything(self) -> None:
        kept, _ = substructure_filter.filter_molecules(self.molecules)
        self.assertEqual(len(kept), 4)

    def test_match_all_include_requires_every_pattern(self) -> None:
        patterns = [
            self.pattern("benzene", "c1ccccc1"),
            self.pattern("acid", "C(=O)[OH]"),
        ]
        any_match, _ = substructure_filter.filter_molecules(
            self.molecules, include_patterns=patterns
        )
        all_match, _ = substructure_filter.filter_molecules(
            self.molecules, include_patterns=patterns, match_all_include=True
        )
        self.assertEqual(self._names(any_match), {"aspirin", "benzene"})
        self.assertEqual(self._names(all_match), {"aspirin"})

    def test_the_report_records_a_status_for_every_molecule(self) -> None:
        _, report = substructure_filter.filter_molecules(
            self.molecules,
            include_patterns=[self.pattern("benzene", "c1ccccc1")],
            exclude_patterns=[self.pattern("acid", "C(=O)[OH]")],
        )
        self.assertEqual(len(report), 4)
        statuses = {entry["status"] for entry in report}
        self.assertEqual(statuses, {"included", "excluded", "no_match"})

    def test_unparseable_molecules_are_skipped_rather_than_crashing(self) -> None:
        kept, report = substructure_filter.filter_molecules(
            [None, *self.molecules]
        )
        self.assertEqual(len(kept), 4)
        self.assertEqual(len(report), 4)


class PropertyTests(unittest.TestCase):
    def test_benzene_has_one_aromatic_ring_and_no_rotatable_bonds(self) -> None:
        properties = molecular_properties.calculate_properties(
            Chem.MolFromSmiles(BENZENE)
        )
        self.assertEqual(properties["Aromatic_Rings"], 1)
        self.assertEqual(properties["Rotatable_Bonds"], 0)
        self.assertEqual(properties["Molecular_Formula"], "C6H6")

    def test_aspirin_reports_its_formula_and_hydrogen_bonding(self) -> None:
        properties = molecular_properties.calculate_properties(
            Chem.MolFromSmiles(ASPIRIN)
        )
        self.assertEqual(properties["Molecular_Formula"], "C9H8O4")
        self.assertEqual(properties["HBD"], 1)  # the carboxylic acid OH
        self.assertGreaterEqual(properties["HBA"], 3)
        self.assertAlmostEqual(properties["MW"], 180.16, delta=0.1)

    def test_heavier_molecules_have_larger_molecular_weight(self) -> None:
        light = molecular_properties.calculate_properties(Chem.MolFromSmiles(ETHANOL))
        heavy = molecular_properties.calculate_properties(Chem.MolFromSmiles(CAFFEINE))
        self.assertLess(light["MW"], heavy["MW"])

    def test_an_unparseable_smiles_is_reported_rather_than_crashing(self) -> None:
        result = molecular_properties.process_single_molecule("not-a-smiles")
        self.assertFalse(result)


class FingerprintTests(unittest.TestCase):
    def setUp(self) -> None:
        self.aspirin = Chem.MolFromSmiles(ASPIRIN)
        self.caffeine = Chem.MolFromSmiles(CAFFEINE)

    def test_every_advertised_method_produces_a_fingerprint(self) -> None:
        for method in similarity_search.FINGERPRINT_METHODS:
            with self.subTest(method=method):
                self.assertIsNotNone(
                    similarity_search.generate_fingerprint(self.aspirin, method)
                )

    def test_the_method_name_is_case_insensitive(self) -> None:
        lower = similarity_search.generate_fingerprint(self.aspirin, "morgan")
        upper = similarity_search.generate_fingerprint(self.aspirin, "MORGAN")
        self.assertEqual(list(lower), list(upper))

    def test_an_unknown_method_is_refused_by_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown fingerprint method: ecfp99"):
            similarity_search.generate_fingerprint(self.aspirin, "ecfp99")

    def test_a_null_molecule_yields_no_fingerprint(self) -> None:
        self.assertIsNone(similarity_search.generate_fingerprint(None))

    def test_a_molecule_is_maximally_similar_to_itself(self) -> None:
        from rdkit import DataStructs

        first = similarity_search.generate_fingerprint(self.aspirin)
        second = similarity_search.generate_fingerprint(self.aspirin)
        self.assertAlmostEqual(
            DataStructs.TanimotoSimilarity(first, second), 1.0, places=9
        )

    def test_different_molecules_are_less_similar_than_identical_ones(self) -> None:
        from rdkit import DataStructs

        aspirin = similarity_search.generate_fingerprint(self.aspirin)
        caffeine = similarity_search.generate_fingerprint(self.caffeine)
        self.assertLess(DataStructs.TanimotoSimilarity(aspirin, caffeine), 1.0)

    def test_the_bit_size_is_honoured(self) -> None:
        small = similarity_search.generate_fingerprint(self.aspirin, "morgan", n_bits=512)
        self.assertEqual(len(small), 512)


class MoleculeLoadingTests(unittest.TestCase):
    def test_a_smiles_file_is_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "molecules.smi"
            path.write_text(f"{ASPIRIN} aspirin\n{BENZENE} benzene\n", encoding="utf-8")
            molecules = similarity_search.load_molecules(str(path))
        self.assertEqual(len(molecules), 2)

    def test_an_unreadable_line_does_not_abort_the_whole_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "molecules.smi"
            path.write_text(
                f"{ASPIRIN} aspirin\nnot-a-smiles junk\n{BENZENE} benzene\n",
                encoding="utf-8",
            )
            molecules = similarity_search.load_molecules(str(path))
        self.assertEqual(len(molecules), 2)


if __name__ == "__main__":
    unittest.main()
