import * as assert from 'assert';
import * as vscode from 'vscode';

suite('KnightBatch Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');

    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('knightbatch-shtest'));
    });

    test('Should activate', async () => {
        const ext = vscode.extensions.getExtension('knightbatch-shtest');
        if (ext) {
            await ext.activate();
            assert.ok(ext.isActive);
        }
    });

    test('Commands should be registered', async () => {
        const commands = await vscode.commands.getCommands();
        assert.ok(commands.includes('knightbatch.compileFile'));
        assert.ok(commands.includes('knightbatch.verifySyntax'));
        assert.ok(commands.includes('knightbatch.showAST'));
        assert.ok(commands.includes('knightbatch.showTokens'));
        assert.ok(commands.includes('knightbatch.compileDirectory'));
        assert.ok(commands.includes('knightbatch.exportToExcel'));
    });
}); 