# Test Coverage Guide

This document explains how to use the test coverage tools for the MCP project, how to interpret the coverage reports, and how the CI integration works.

## Running Test Coverage Locally

### Prerequisites

Make sure you have the required dependencies installed:

```bash
pip install -e ".[dev]"
```

This will install pytest, coverage.py, and other development dependencies.

### Running the Coverage Script

The project includes a dedicated script for running test coverage:

```bash
python scripts/run_coverage.py
```

This will:
1. Run all tests in the `tests/` directory
2. Measure code coverage for the `mcp_units` package
3. Display a coverage report in the terminal

### Additional Options

The coverage script supports several options:

- Generate an HTML report:
  ```bash
  python scripts/run_coverage.py --html
  ```

- Generate an XML report (useful for CI integration):
  ```bash
  python scripts/run_coverage.py --xml
  ```

- Specify a custom output directory:
  ```bash
  python scripts/run_coverage.py --html --output my_coverage_reports
  ```

### Manual Coverage Commands

If you prefer to run the coverage commands directly:

1. Run the tests with coverage:
   ```bash
   coverage run --source=mcp_units -m pytest tests/
   ```

2. Generate a terminal report:
   ```bash
   coverage report -m
   ```

3. Generate an HTML report:
   ```bash
   coverage html
   ```

4. Open the HTML report in your browser:
   ```bash
   # On Windows
   start htmlcov/index.html
   
   # On macOS
   open htmlcov/index.html
   
   # On Linux
   xdg-open htmlcov/index.html
   ```

## Interpreting Coverage Reports

### Terminal Report

The terminal report shows a summary of coverage for each module:

```
Name                                      Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------
mcp_units/mcp_agent_interaction_engine/dialog_flow.py      45     10    78%   24-27, 35-40
mcp_units/mcp_host_llm_infer/llm_service.py                38      5    87%   45-50
...
-----------------------------------------------------------------------
TOTAL                                      213     35    84%
```

- **Stmts**: Total number of statements in the module
- **Miss**: Number of statements not covered by tests
- **Cover**: Percentage of statements covered
- **Missing**: Line numbers of statements not covered

### HTML Report

The HTML report provides a more detailed view:

1. Open `coverage_reports/html/index.html` in your browser
2. The main page shows an overview of all modules
3. Click on a module to see line-by-line coverage
4. Lines highlighted in red are not covered by tests
5. Lines highlighted in green are covered

## CI Integration

The project includes GitHub Actions workflow for automated test coverage:

### Workflow File

The workflow is defined in `.github/workflows/test-coverage.yaml` and:

1. Runs on push to the main branch and on pull requests
2. Sets up Python and installs dependencies
3. Runs tests with coverage
4. Generates coverage reports (terminal, XML, HTML)
5. Uploads the reports as artifacts
6. Checks if coverage meets the minimum threshold

### Viewing CI Results

After a workflow run:

1. Go to the GitHub Actions tab in the repository
2. Select the "Test Coverage" workflow
3. Download the coverage report artifact
4. Extract and open `coverage_html/index.html`

### Coverage Threshold

The CI workflow checks if the total coverage meets a minimum threshold (currently 50%). This threshold can be adjusted as test coverage improves.

## Recommendations for Maintaining High Test Coverage

1. **Write Tests First**: Follow a test-driven development approach when adding new features.

2. **Focus on Critical Components**: Prioritize testing for core functionality and error-prone areas.

3. **Address Uncovered Code**: Regularly review coverage reports and add tests for uncovered code.

4. **Test Edge Cases**: Ensure tests cover both normal operation and edge cases.

5. **Integration Tests**: Add tests that verify interactions between different MCP components.

6. **Maintain the Threshold**: Gradually increase the coverage threshold as coverage improves.

7. **Review Coverage on PRs**: Make reviewing coverage reports part of the PR review process.

## Continuous Compliance

This test coverage solution addresses the continuous compliance requirements by:

1. Providing metrics on test coverage
2. Identifying areas of code not covered by tests
3. Integrating with CI to ensure coverage doesn't decrease
4. Documenting the process for maintaining high test coverage

By following these guidelines, the project can maintain high test coverage and ensure continuous compliance with MCP requirements.