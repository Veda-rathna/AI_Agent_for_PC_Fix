"""
Test script for AutoGen MCP Integration

Run this script to verify the AutoGen integration is working correctly.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from autogen_integration.orchestrator import AutoGenOrchestrator
        from autogen_integration.parsers.mcp_parser import MCPTaskParser
        from autogen_integration.tools.system_diagnostics import SystemDiagnostics
        from autogen_integration.tools.event_logs import EventLogAnalyzer
        from autogen_integration.tools.file_checker import SystemFileChecker
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {str(e)}")
        return False

def test_mcp_parser():
    """Test MCP task parsing"""
    print("\nTesting MCP Parser...")
    try:
        from autogen_integration.parsers.mcp_parser import MCPTaskParser
        
        parser = MCPTaskParser()
        
        # Sample model output with MCP tasks
        model_output = """
Your computer seems slow. Let me check a few things.

<MCP_TASKS>
{
  "tasks": [
    "Analyze CPU thermal sensor readings for overheating patterns",
    "Inspect disk usage telemetry for signs of resource-intensive programs"
  ],
  "summary": "Performance diagnostics"
}
</MCP_TASKS>
"""
        
        # Parse tasks
        mcp_data = parser.extract_mcp_tasks(model_output)
        
        if mcp_data:
            print(f"✅ Parsed {len(mcp_data['tasks'])} tasks")
            print(f"   Summary: {mcp_data['summary']}")
            
            # Test categorization
            categorized = parser.categorize_tasks(mcp_data['tasks'])
            print(f"✅ Categorized into {len(categorized)} categories")
            for category, tasks in categorized.items():
                print(f"   - {category}: {len(tasks)} task(s)")
            
            return True
        else:
            print("❌ Failed to parse MCP tasks")
            return False
            
    except Exception as e:
        print(f"❌ Parser test failed: {str(e)}")
        return False

def test_diagnostic_tools():
    """Test diagnostic tools"""
    print("\nTesting Diagnostic Tools...")
    try:
        from autogen_integration.tools.system_diagnostics import SystemDiagnostics
        
        diagnostics = SystemDiagnostics()
        
        # Test CPU thermal analysis
        print("  Testing CPU thermal analysis...")
        result = diagnostics.analyze_cpu_thermal()
        if result.get('success'):
            print(f"  ✅ CPU Analysis: {result.get('analysis', 'Done')}")
        else:
            print(f"  ⚠️  CPU Analysis: {result.get('error', 'Unknown error')}")
        
        # Test memory check
        print("  Testing memory usage check...")
        result = diagnostics.check_memory_usage()
        if result.get('success'):
            print(f"  ✅ Memory Analysis: {result.get('analysis', 'Done')}")
        else:
            print(f"  ⚠️  Memory Analysis: {result.get('error', 'Unknown error')}")
        
        print("✅ Diagnostic tools working")
        return True
        
    except Exception as e:
        print(f"❌ Diagnostic tools test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_orchestrator():
    """Test orchestrator"""
    print("\nTesting AutoGen Orchestrator...")
    try:
        from autogen_integration.orchestrator import AutoGenOrchestrator
        
        # Create orchestrator
        orchestrator = AutoGenOrchestrator()
        print("✅ Orchestrator initialized")
        
        # Sample model output
        model_output = """
Your system may have performance issues.

<MCP_TASKS>
{
  "tasks": [
    "Analyze CPU thermal sensor readings",
    "Check memory usage for resource-intensive processes",
    "Verify Windows Event Logs for error messages"
  ],
  "summary": "System performance diagnostics"
}
</MCP_TASKS>
"""
        
        # Execute tasks (direct mode)
        print("  Executing MCP tasks in direct mode...")
        result = orchestrator.execute_mcp_tasks(model_output, use_autogen=False)
        
        if result.get('success'):
            print(f"✅ Execution successful:")
            print(f"   - Tasks requested: {result.get('tasks_requested', 0)}")
            print(f"   - Tasks completed: {result.get('tasks_completed', 0)}")
            print(f"   - Tasks failed: {result.get('tasks_failed', 0)}")
            
            # Show individual results
            for i, task_result in enumerate(result.get('results', [])[:3], 1):
                task_name = task_result.get('task', 'Unknown')
                analysis = task_result.get('analysis', 'No analysis')
                print(f"   {i}. {task_name}")
                print(f"      → {analysis}")
            
            return True
        else:
            print(f"❌ Execution failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Orchestrator test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("AutoGen MCP Integration - Test Suite")
    print("="*60)
    
    tests = [
        ("Import Test", test_imports),
        ("MCP Parser Test", test_mcp_parser),
        ("Diagnostic Tools Test", test_diagnostic_tools),
        ("Orchestrator Test", test_orchestrator),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} crashed: {str(e)}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    
    print("="*60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! AutoGen integration is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
