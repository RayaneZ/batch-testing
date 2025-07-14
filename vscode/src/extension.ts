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
    let runTests = vscode.commands.registerCommand('knightbatch.runTests', runTestSuite);

    context.subscriptions.push(compileFile, verifySyntax, showAST, showTokens, compileDirectory, exportToExcel, runTests);
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

        // Use the new module-based approach
        const args = ['-m', 'shtest_compiler.compile_file', filePath, '--output', outputPath];
        if (debugMode) {
            args.push('--debug');
        }

        const result = await executeKnightBatchCommand('python', args, workspaceFolder.uri.fsPath);
        
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
    const workspaceFolder = vscode.workspace.getWorkspaceFolder(editor.document.uri);
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder found');
        return;
    }

    try {
        // Use the new module-based approach
        const args = ['-m', 'shtest_compiler.verify_syntax', filePath];
        const result = await executeKnightBatchCommand('python', args, workspaceFolder.uri.fsPath);
        
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
    const workspaceFolder = vscode.workspace.getWorkspaceFolder(editor.document.uri);
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder found');
        return;
    }

    try {
        // Use the new module-based approach with debug output
        const args = ['-m', 'shtest_compiler.compile_file', filePath, '--ast', '--debug'];
        const result = await executeKnightBatchCommand('python', args, workspaceFolder.uri.fsPath);
        
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
    const workspaceFolder = vscode.workspace.getWorkspaceFolder(editor.document.uri);
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder found');
        return;
    }

    try {
        // Use the new module-based approach with debug output
        const args = ['-m', 'shtest_compiler.compile_file', filePath, '--tokens', '--debug'];
        const result = await executeKnightBatchCommand('python', args, workspaceFolder.uri.fsPath);
        
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

        // Use the new module-based approach
        const args = ['-m', 'shtest_compiler.generate_tests', '--input-dir', workspaceFolder.uri.fsPath, '--output', outputPath];
        if (debugMode) {
            args.push('--debug');
        }

        const result = await executeKnightBatchCommand('python', args, workspaceFolder.uri.fsPath);
        
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
        const args = ['-m', 'shtest_compiler.export_to_excel', '--input-dir', workspaceFolder.uri.fsPath, '--output', outputFile];

        const result = await executeKnightBatchCommand('python', args, workspaceFolder.uri.fsPath);
        
        if (result.success) {
            vscode.window.showInformationMessage(`Exported ${files.length} files to ${outputFile}`);
        } else {
            vscode.window.showErrorMessage(`Export failed: ${result.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error exporting to Excel: ${error}`);
    }
}

async function runTestSuite() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder found');
        return;
    }

    try {
        // Run the test suite using pytest
        const args = ['-m', 'pytest', 'testing/', '-v', '--tb=short'];
        const result = await executeKnightBatchCommand('python', args, workspaceFolder.uri.fsPath);
        
        if (result.success) {
            vscode.window.showInformationMessage('Test suite completed successfully');
            
            // Show test results in a new document
            const doc = await vscode.workspace.openTextDocument({
                content: result.output,
                language: 'text'
            });
            await vscode.window.showTextDocument(doc, { preview: true });
        } else {
            vscode.window.showErrorMessage(`Test suite failed: ${result.error}`);
            
            // Show error output in a new document
            const doc = await vscode.workspace.openTextDocument({
                content: result.error,
                language: 'text'
            });
            await vscode.window.showTextDocument(doc, { preview: true });
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error running test suite: ${error}`);
    }
}

async function executeKnightBatchCommand(command: string, args: string[], workspacePath: string): Promise<{ success: boolean; output: string; error: string }> {
    return new Promise((resolve) => {
        const process = spawn(command, args, {
            cwd: workspacePath,
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