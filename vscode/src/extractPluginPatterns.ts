import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

// Chemin racine du projet (adapter si besoin)
const PROJECT_ROOT = path.resolve(__dirname, '../../');
const PLUGINS_DIR = path.join(PROJECT_ROOT, 'src/shtest_compiler/plugins');
const OUTPUT_JSON = path.join(__dirname, '../plugin_patterns.json');

interface PluginPattern {
  plugin: string;
  category: string;
  handler: string;
  pattern: string;
  scope?: string;
}

interface PatternEntry {
  handler: string;
  pattern: string;
  scope?: string;
}

function extractPatternsFromYml(ymlPath: string, plugin: string): PluginPattern[] {
  const content = fs.readFileSync(ymlPath, 'utf-8');
  const doc = yaml.load(content) as unknown;
  const patterns: PluginPattern[] = [];
  if (!doc || typeof doc !== 'object' || doc === null || !('patterns' in doc)) {return patterns;}
  const docWithPatterns = doc as { patterns: Record<string, PatternEntry[]> };
  for (const category of Object.keys(docWithPatterns.patterns)) {
    for (const entry of docWithPatterns.patterns[category]) {
      patterns.push({
        plugin,
        category,
        handler: entry.handler,
        pattern: entry.pattern,
        scope: entry.scope,
      });
    }
  }
  return patterns;
}

function main(): void {
  const plugins = fs.readdirSync(PLUGINS_DIR).filter((f: string) => fs.statSync(path.join(PLUGINS_DIR, f)).isDirectory());
  const allPatterns: PluginPattern[] = [];
  for (const plugin of plugins) {
    const configDir = path.join(PLUGINS_DIR, plugin, 'config');
    if (!fs.existsSync(configDir)) {continue;}
    const ymlFiles = fs.readdirSync(configDir).filter((f: string) => f.startsWith('patterns_') && f.endsWith('.yml'));
    for (const ymlFile of ymlFiles) {
      const ymlPath = path.join(configDir, ymlFile);
      const patterns = extractPatternsFromYml(ymlPath, plugin);
      allPatterns.push(...patterns);
    }
  }
  fs.writeFileSync(OUTPUT_JSON, JSON.stringify(allPatterns, null, 2), 'utf-8');
  console.log(`✅ Plugin patterns exported to ${OUTPUT_JSON} (${allPatterns.length} patterns)`);
}

main(); 