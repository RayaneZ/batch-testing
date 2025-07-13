import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn } from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    console.log('KnightBatch extension is now active!');

    // Register commands
    let compileFile = vscode.commands.registerCommand('knightbatch.compileFile', compileCurrentFile);
    let verifySyntax = vscode.commands.registerCommand('knightbatch.verifySyntax', verifyCurrentFile);
    let showAST = vscode.commands.registerCommand('knightbatch.showAST', showASTForFile);
    let showTokens = vscode.commands.registerCommand('knightbatch.showTokens', showTokensForFile);
    let compileDirectory = vscode.commands.registerCommand('knightbatch.compileDirectory', compileDirectoryCommand);
    let exportToExcel = vscode.commands.registerCommand('knightbatch.exportToExcel', exportToExcelCommand);

    context.subscriptions.push(compileFile, verifySyntax, showAST, showTokens, compileDirectory, exportToExcel);
}

export function deactivate() {}

async function compileCurrentFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'shtest') {
        vscode.window.showErrorMessage('No .shtest file is currently active');
        return;
    }

    const filePath = editor.document.fileName;
    const config = vscode.workspace.getConfiguration('knightbatch');
    const outputDir = config.get<string>('outputDirectory', 'output');
    const debugMode = config.get<boolean>('debugMode', false);

    try {
        // Ensure output directory exists
        const workspaceFolder = vscode.workspace.getWorkspaceFolder(editor.document.uri);
        if (!workspaceFolder) {
            vscode.window.showErrorMessage('No workspace folder found');
            return;
        }

        const outputPath = path.join(workspaceFolder.uri.fsPath, outputDir);
        if (!fs.existsSync(outputPath)) {
            fs.mkdirSync(outputPath, { recursive: true });
        }

        // Build command
        const args = [filePath, '--output', outputPath];
        if (debugMode) {
            args.push('--debug');
        }

        const result = await executeKnightBatchCommand('shtest.py', args);
        
        if (result.success) {
            vscode.window.showInformationMessage(`File compiled successfully to ${outputPath}`);
            
            // Show the generated file
            const outputFile = path.join(outputPath, path.basename(filePath, '.shtest') + '.sh');
            if (fs.existsSync(outputFile)) {
                const doc = await vscode.workspace.openTextDocument(outputFile);
                await vscode.window.showTextDocument(doc, { preview: true });
            }
        } else {
            vscode.window.showErrorMessage(`Compilation failed: ${result.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error compiling file: ${error}`);
    }
}

async function verifyCurrentFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'shtest') {
        vscode.window.showErrorMessage('No .shtest file is currently active');
        return;
    }

    const filePath = editor.document.fileName;
    const config = vscode.workspace.getConfiguration('knightbatch');
    const configPath = config.get<string>('configPath', 'config/patterns_actions.yml');

    try {
        const args = [filePath, '--config', configPath];
        const result = await executeKnightBatchCommand('verify_syntax.py', args);
        
        if (result.success) {
            vscode.window.showInformationMessage('Syntax verification passed');
        } else {
            vscode.window.showErrorMessage(`Syntax verification failed: ${result.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error verifying syntax: ${error}`);
    }
}

async function showASTForFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'shtest') {
        vscode.window.showErrorMessage('No .shtest file is currently active');
        return;
    }

    const filePath = editor.document.fileName;
    const config = vscode.workspace.getConfiguration('knightbatch');
    const configPath = config.get<string>('configPath', 'config/patterns_actions.yml');

    try {
        const args = [filePath, '--ast', '--config', configPath];
        const result = await executeKnightBatchCommand('shtest.py', args);
        
        if (result.success) {
            // Create a new document to show the AST
            const doc = await vscode.workspace.openTextDocument({
                content: result.output,
                language: 'json'
            });
            await vscode.window.showTextDocument(doc, { preview: true });
        } else {
            vscode.window.showErrorMessage(`Failed to generate AST: ${result.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error generating AST: ${error}`);
    }
}

async function showTokensForFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'shtest') {
        vscode.window.showErrorMessage('No .shtest file is currently active');
        return;
    }

    const filePath = editor.document.fileName;
    const config = vscode.workspace.getConfiguration('knightbatch');
    const configPath = config.get<string>('configPath', 'config/patterns_actions.yml');

    try {
        const args = [filePath, '--tokens', '--config', configPath];
        const result = await executeKnightBatchCommand('shtest.py', args);
        
        if (result.success) {
            // Create a new document to show the tokens
            const doc = await vscode.workspace.openTextDocument({
                content: result.output,
                language: 'json'
            });
            await vscode.window.showTextDocument(doc, { preview: true });
        } else {
            vscode.window.showErrorMessage(`Failed to generate tokens: ${result.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error generating tokens: ${error}`);
    }
}

async function compileDirectoryCommand() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder found');
        return;
    }

    const config = vscode.workspace.getConfiguration('knightbatch');
    const outputDir = config.get<string>('outputDirectory', 'output');
    const debugMode = config.get<boolean>('debugMode', false);

    try {
        // Find all .shtest files in the workspace
        const pattern = new vscode.RelativePattern(workspaceFolder, '**/*.shtest');
        const files = await vscode.workspace.findFiles(pattern);
        
        if (files.length === 0) {
            vscode.window.showInformationMessage('No .shtest files found in workspace');
            return;
        }

        const outputPath = path.join(workspaceFolder.uri.fsPath, outputDir);
        if (!fs.existsSync(outputPath)) {
            fs.mkdirSync(outputPath, { recursive: true });
        }

        // Build command
        const args = ['--input-dir', workspaceFolder.uri.fsPath, '--output', outputPath];
        if (debugMode) {
            args.push('--debug');
        }

        const result = await executeKnightBatchCommand('generate_tests.py', args);
        
        if (result.success) {
            vscode.window.showInformationMessage(`Compiled ${files.length} files to ${outputPath}`);
        } else {
            vscode.window.showErrorMessage(`Compilation failed: ${result.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error compiling directory: ${error}`);
    }
}

async function exportToExcelCommand() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder found');
        return;
    }

    try {
        // Find all .shtest files in the workspace
        const pattern = new vscode.RelativePattern(workspaceFolder, '**/*.shtest');
        const files = await vscode.workspace.findFiles(pattern);
        
        if (files.length === 0) {
            vscode.window.showInformationMessage('No .shtest files found in workspace');
            return;
        }

        const outputFile = path.join(workspaceFolder.uri.fsPath, 'tests.xlsx');
        const args = ['--input-dir', workspaceFolder.uri.fsPath, '--output', outputFile];

        const result = await executeKnightBatchCommand('export_to_excel.py', args);
        
        if (result.success) {
            vscode.window.showInformationMessage(`Exported ${files.length} files to ${outputFile}`);
        } else {
            vscode.window.showErrorMessage(`Export failed: ${result.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error exporting to Excel: ${error}`);
    }
}

async function executeKnightBatchCommand(script: string, args: string[]): Promise<{ success: boolean; output: string; error: string }> {
    return new Promise((resolve) => {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            resolve({ success: false, output: '', error: 'No workspace folder found' });
            return;
        }

        const scriptPath = path.join(workspaceFolder.uri.fsPath, 'src', script);
        
        if (!fs.existsSync(scriptPath)) {
            resolve({ success: false, output: '', error: `Script not found: ${scriptPath}` });
            return;
        }

        const process = spawn('python', [scriptPath, ...args], {
            cwd: path.join(workspaceFolder.uri.fsPath, 'src'),
            stdio: ['pipe', 'pipe', 'pipe']
        });

        let output = '';
        let error = '';

        process.stdout.on('data', (data) => {
            output += data.toString();
        });

        process.stderr.on('data', (data) => {
            error += data.toString();
        });

        process.on('close', (code) => {
            if (code === 0) {
                resolve({ success: true, output, error });
            } else {
                resolve({ success: false, output, error: error || `Process exited with code ${code}` });
            }
        });

        process.on('error', (err) => {
            resolve({ success: false, output, error: err.message });
        });
    });
} 