#!/usr/bin/env python3
print("Starting simple test...")

try:
    print("Importing parser...")
    from shtest_compiler.parser.parser import Parser
    print("Parser imported successfully")
    
    print("Creating parser instance...")
    parser = Parser()
    print("Parser created successfully")
    
    print("Testing with simple content...")
    content = "Étape: Test\nAction: echo 'test'\nRésultat: stdout contient 'test'"
    parser.parse(content, path="test.shtest", debug=False)
    print("Parse successful!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.") 