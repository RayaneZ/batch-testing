# PowerShell test suite for shtest_compiler
# Supports Windows with WSL integration

param(
    [string]$ProjectRoot = "..",
    [switch]$NoShellcheck,
    [switch]$UnitOnly,
    [switch]$E2EOnly,
    [switch]$IntegrationOnly,
    [switch]$QualityOnly,
    [switch]$ShellcheckOnly,
    [switch]$Help
)

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Test-WSLAvailability {
    try {
        $result = & wsl --version 2>$null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

function Install-Shellcheck {
    Write-ColorOutput Green "Installing shellcheck in WSL..."
    try {
        & wsl sudo apt-get update
        & wsl sudo apt-get install -y shellcheck
        Write-ColorOutput Green "Shellcheck installed successfully in WSL"
        return $true
    }
    catch {
        Write-ColorOutput Red "Failed to install shellcheck: $_"
        return $false
    }
}

function Run-UnitTests {
    Write-ColorOutput Yellow "🧪 Running unit tests..."
    $cmd = @("python", "-m", "pytest", "testing/tests/unit/", "-v", "--cov=shtest_compiler", "--cov-report=term-missing")
    & $cmd[0] $cmd[1..($cmd.Length-1)]
    return $LASTEXITCODE -eq 0
}

function Compile-E2ETests {
    Write-ColorOutput Yellow "🔨 Compiling E2E tests..."
    $cmd = @("python", "-m", "shtest_compiler.run_all", "--input", "testing/tests/e2e", "--output", "testing/tests/integration")
    & $cmd[0] $cmd[1..($cmd.Length-1)]
    return $LASTEXITCODE -eq 0
}

function Run-Shellcheck {
    Write-ColorOutput Yellow "🔍 Running shellcheck on compiled scripts..."
    
    if (-not (Test-WSLAvailability)) {
        Write-ColorOutput Red "WSL not available. Skipping shellcheck."
        return $false
    }
    
    $integrationDir = Join-Path $ProjectRoot "src\testing\tests\integration"
    if (-not (Test-Path $integrationDir)) {
        Write-ColorOutput Yellow "Integration directory not found. Skipping shellcheck."
        return $true
    }
    
    $shellScripts = Get-ChildItem -Path $integrationDir -Filter "*.sh"
    if ($shellScripts.Count -eq 0) {
        Write-ColorOutput Yellow "No shell scripts found. Skipping shellcheck."
        return $true
    }
    
    $allPassed = $true
    foreach ($script in $shellScripts) {
        Write-Output "Checking $($script.Name)..."
        $result = & wsl shellcheck --shell=bash --severity=style $script.FullName
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput Red "Shellcheck failed for $($script.Name)"
            $allPassed = $false
        }
    }
    
    return $allPassed
}

function Run-IntegrationTests {
    Write-ColorOutput Yellow "🔗 Running integration tests..."
    
    $integrationDir = Join-Path $ProjectRoot "src\testing\tests\integration"
    if (-not (Test-Path $integrationDir)) {
        Write-ColorOutput Yellow "Integration directory not found. Skipping integration tests."
        return $true
    }
    
    $shellScripts = Get-ChildItem -Path $integrationDir -Filter "*.sh"
    if ($shellScripts.Count -eq 0) {
        Write-ColorOutput Yellow "No shell scripts found. Skipping integration tests."
        return $true
    }
    
    $allPassed = $true
    foreach ($script in $shellScripts) {
        Write-Output "Running $($script.Name)..."
        $result = & wsl bash $script.FullName
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput Red "Integration test failed for $($script.Name)"
            $allPassed = $false
        }
    }
    
    return $allPassed
}

function Run-QualityChecks {
    Write-ColorOutput Yellow "✨ Running code quality checks..."
    
    $allPassed = $true
    
    # Black formatting check
    Write-Output "Checking code formatting with black..."
    $result = & python -m black --check shtest_compiler/ testing/tests/
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput Red "Black formatting check failed"
        $allPassed = $false
    }
    
    # Flake8 linting
    Write-Output "Running flake8 linting..."
    $result = & python -m flake8 shtest_compiler/ testing/tests/
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput Red "Flake8 linting failed"
        $allPassed = $false
    }
    
    # MyPy type checking
    Write-Output "Running mypy type checking..."
    $result = & python -m mypy shtest_compiler/
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput Red "MyPy type checking failed"
        $allPassed = $false
    }
    
    return $allPassed
}

function Show-Help {
    Write-Output @"
PowerShell Test Suite for shtest_compiler

Usage: .\test_suite.ps1 [options]

Options:
    -ProjectRoot <path>     Project root directory (default: parent directory)
    -NoShellcheck          Skip shellcheck validation
    -UnitOnly              Run unit tests only
    -E2EOnly               Compile E2E tests only
    -IntegrationOnly       Run integration tests only
    -QualityOnly           Run code quality checks only
    -ShellcheckOnly        Run shellcheck only
    -Help                  Show this help message

Examples:
    .\test_suite.ps1                    # Run all tests
    .\test_suite.ps1 -UnitOnly          # Run unit tests only
    .\test_suite.ps1 -NoShellcheck      # Run all tests except shellcheck
    .\test_suite.ps1 -ProjectRoot "C:\path\to\project"

"@
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

# Change to project root
Set-Location $ProjectRoot

Write-ColorOutput Cyan "🚀 Starting PowerShell test suite for shtest_compiler..."
Write-Output "📁 Project root: $(Get-Location)"
Write-Output "🖥️  Platform: Windows"
Write-Output "🐧 WSL available: $(if (Test-WSLAvailability) { 'Yes' } else { 'No' })"
Write-Output ""

$startTime = Get-Date
$allPassed = $true

try {
    # Check if we're in the right directory
    if (-not (Test-Path "src\shtest_compiler")) {
        Write-ColorOutput Red "❌ Error: Could not find shtest_compiler in the specified directory"
        exit 1
    }
    
    # Change to src directory for test execution
    Set-Location "src"
    
    # Run specific test types based on parameters
    if ($UnitOnly) {
        $allPassed = Run-UnitTests
    }
    elseif ($E2EOnly) {
        $allPassed = Compile-E2ETests
    }
    elseif ($IntegrationOnly) {
        $allPassed = Run-IntegrationTests
    }
    elseif ($QualityOnly) {
        $allPassed = Run-QualityChecks
    }
    elseif ($ShellcheckOnly) {
        $allPassed = Run-Shellcheck
    }
    else {
        # Run all tests
        Write-ColorOutput Yellow "Running complete test suite..."
        
        # Unit tests
        if (-not (Run-UnitTests)) {
            $allPassed = $false
        }
        
        # Compile E2E tests
        if (-not (Compile-E2ETests)) {
            $allPassed = $false
        }
        
        # Shellcheck (if enabled)
        if (-not $NoShellcheck) {
            if (-not (Run-Shellcheck)) {
                $allPassed = $false
            }
        }
        
        # Integration tests
        if (-not (Run-IntegrationTests)) {
            $allPassed = $false
        }
        
        # Quality checks
        if (-not (Run-QualityChecks)) {
            $allPassed = $false
        }
    }
    
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    Write-Output ""
    Write-ColorOutput Cyan "📊 Test Summary:"
    Write-Output "   Duration: $($duration.TotalSeconds.ToString('F2'))s"
    
    if ($allPassed) {
        Write-ColorOutput Green "✅ All tests passed!"
        exit 0
    } else {
        Write-ColorOutput Red "❌ Some tests failed!"
        exit 1
    }
    
}
catch {
    Write-ColorOutput Red "💥 Test suite failed with error: $_"
    exit 1
}
finally {
    # Return to original directory
    Set-Location $ProjectRoot
} 