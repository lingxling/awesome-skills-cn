import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const require = createRequire(import.meta.url);
const { findProjectRoot } = require('../lib/project-root');
const { resolveSafeRealPath } = require('../lib/symlink-safety');

const ROOT_DIR = findProjectRoot(__dirname);
const WEB_APP_PUBLIC = path.join(ROOT_DIR, 'apps', 'web-app', 'public');

// 2. Copy skills directory content
// Note: Symlinking is better, but Windows often requires admin for symlinks. 
// We will try to copy for reliability in this environment.
function copyFolderSync(from, to, rootDir = from) {
    if (!fs.existsSync(to)) fs.mkdirSync(to, { recursive: true });

    fs.readdirSync(from).forEach(element => {
        const srcPath = path.join(from, element);
        const destPath = path.join(to, element);
        const stat = fs.lstatSync(srcPath);
        const realPath = stat.isSymbolicLink() ? resolveSafeRealPath(rootDir, srcPath) : srcPath;

        if (!realPath) {
            console.warn(`[app:setup] Skipping symlink outside skills root: ${srcPath}`);
            return;
        }

        const realStat = fs.statSync(realPath);

        if (realStat.isFile()) {
            fs.copyFileSync(realPath, destPath);
        } else if (realStat.isDirectory()) {
            copyFolderSync(realPath, destPath, rootDir);
        }
        // Skip other types (e.g. sockets, FIFOs)
    });
}

function copyIndexFiles(sourceIndex, destIndex, destBackupIndex) {
    console.log(`Copying ${sourceIndex} -> ${destIndex}...`);
    fs.copyFileSync(sourceIndex, destIndex);

    console.log(`Copying ${sourceIndex} -> ${destBackupIndex}...`);
    fs.copyFileSync(sourceIndex, destBackupIndex);
}

function main() {
    if (!fs.existsSync(WEB_APP_PUBLIC)) {
        fs.mkdirSync(WEB_APP_PUBLIC, { recursive: true });
    }

    const sourceIndex = path.join(ROOT_DIR, 'skills_index.json');
    const destIndex = path.join(WEB_APP_PUBLIC, 'skills.json');
    const destBackupIndex = path.join(WEB_APP_PUBLIC, 'skills.json.backup');
    copyIndexFiles(sourceIndex, destIndex, destBackupIndex);

    const sourceSkills = path.join(ROOT_DIR, 'skills');
    const destSkills = path.join(WEB_APP_PUBLIC, 'skills');

    console.log(`Copying skills directory...`);

    // Check if destination exists and remove it to ensure fresh copy
    if (fs.existsSync(destSkills)) {
        fs.rmSync(destSkills, { recursive: true, force: true });
    }

    copyFolderSync(sourceSkills, destSkills, sourceSkills);

    console.log('✅ Web app assets setup complete!');
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    main();
}

export { copyFolderSync, copyIndexFiles, main };
