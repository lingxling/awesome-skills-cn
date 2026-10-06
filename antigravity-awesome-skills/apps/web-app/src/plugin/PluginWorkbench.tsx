import { useEffect, useState } from 'react';
import { App } from '@modelcontextprotocol/ext-apps';
import { Workbench, type WorkbenchHostArtifacts } from '../pages/Workbench';

export function PluginWorkbench(): React.ReactElement {
  const [artifacts, setArtifacts] = useState<WorkbenchHostArtifacts>();
  const [status, setStatus] = useState('Local files stay in this view. Connecting to the plugin host…');
  useEffect(() => {
    if (window.parent === window) { setStatus('Standalone preview. Explicitly import your artifacts below.'); return; }
    const app = new App({ name: 'AAS Workbench', version: '0.1.0' }, {}, { autoResize: true });
    let current = true;
    app.ontoolresult = (result) => {
      if (!current) return;
      const content = result.structuredContent;
      if (result.isError || !content || typeof content !== 'object' || Array.isArray(content)) {
        setArtifacts({}); setStatus('The tool result could not be reviewed. Import an artifact explicitly.'); return;
      }
      const values = content as Record<string, unknown>;
      setArtifacts({ manifest: values.manifest, plan: values.plan, evidence: values.evidence });
      setStatus('Reviewing the current tool result. Local imports stay in this view.');
    };
    void app.connect().catch(() => { if (current) setStatus('Host connection unavailable. Explicit file review still works.'); });
    return () => { current = false; void app.close(); };
  }, []);
  return <><p className="plugin-status" role="status">{status}</p><Workbench embedded hostArtifacts={artifacts} /></>;
}
