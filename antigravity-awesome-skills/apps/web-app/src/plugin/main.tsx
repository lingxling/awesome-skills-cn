import { createRoot } from 'react-dom/client';
import { MemoryRouter } from 'react-router';
import { PluginWorkbench } from './PluginWorkbench';
import '../index.css';
import './plugin.css';
createRoot(document.getElementById('root')!).render(<MemoryRouter><PluginWorkbench /></MemoryRouter>);
