# AWS EC2 Cost Optimization Analyzer

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A comprehensive Python tool designed to identify cost optimization opportunities for AWS EC2 instances by analyzing usage patterns, costs, and resource utilization.

> 🇯🇵 **日本語版**: [README_ja.md](README_ja.md) をご覧ください

## 🚀 Features

- **Smart Cost Analysis**: Two-tier priority system for optimization opportunities
- **Comprehensive Monitoring**: CPU utilization and network activity analysis
- **Cost Calculation**: Real-time cost estimation with potential savings
- **Easy Setup**: Automated Python environment setup with batch scripts
- **Flexible Reporting**: Console output and JSON export options
- **Multi-Region Support**: Analyze instances across different AWS regions

### Analysis Priorities

1. **🚨 High Priority**: Expensive instances (>$100/month) running 24+ hours
2. **⚠️ Medium Priority**: Long-term running instances (30+ days)

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Sample Output](#sample-output)
- [Analysis Criteria](#analysis-criteria)
- [Contributing](#contributing)
- [License](#license)

> 📖 **Detailed Installation Guide**: [docs/INSTALLATION.md](docs/INSTALLATION.md) | [日本語版](docs/INSTALLATION_ja.md)

## 📋 Prerequisites

### System Requirements
- **Windows 10/11** (Windows Server also supported)
- **Python 3.7+** (automatically detected and installed if needed)
- **AWS CLI** (optional, can use environment variables)

### AWS Requirements
- **AWS Account** with EC2 instances
- **IAM Permissions**:
  - `ec2:DescribeInstances`
  - `cloudwatch:GetMetricStatistics`

### AWS Authentication (Choose one method)

#### Method 1: AWS CLI
```cmd
aws configure
```

#### Method 2: Environment Variables
```cmd
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_DEFAULT_REGION=ap-northeast-1
```

#### Method 3: IAM Role (for EC2 instances)
Attach an IAM role with the required permissions to your EC2 instance.

## 🚀 Quick Start

### One-Command Setup (Recommended)
```cmd
start.bat
```
This single command will:
- Auto-detect Python (with installation guidance if not found)
- Create virtual environment automatically
- Install required packages
- Present execution options menu

### Manual Setup (Alternative)

#### Step 1: Install Python (if needed)
```cmd
install_python.bat
```
*Run as administrator for automatic Python installation*

#### Step 2: Environment Setup
```cmd
setup.bat
```
Creates virtual environment and installs dependencies

## 💻 Usage

### Basic Execution
```cmd
run.bat
```

### Advanced Options
```cmd
# Analyze specific region
run.bat --region us-west-2

# Change analysis period (last 7 days)
run.bat --days 7

# Adjust CPU threshold (target <10% utilization)
run.bat --cpu-threshold 10.0

# Set expensive instance threshold ($200+/month)
run.bat --expensive-threshold 200.0

# Export results to JSON
run.bat --output cost_analysis.json

# Combined options
run.bat --region ap-northeast-1 --days 14 --cpu-threshold 3.0 --expensive-threshold 150.0 --output report.json
```

### Interactive Mode
```cmd
run_with_options.bat
```
*Menu-driven interface for setting all options*

### Cleanup
```cmd
clean.bat
```
*Removes virtual environment*

## 📁 Project Structure

```
aws-ec2-cost-analyzer/
├── 📄 ec2_usage_analyzer.py    # Main analysis script
├── 📄 requirements.txt         # Python dependencies
├── 🚀 start.bat               # One-command startup
├── ⚙️ setup.bat               # Environment setup
├── ▶️ run.bat                 # Basic execution
├── 🎛️ run_with_options.bat    # Interactive execution
├── 🐍 install_python.bat      # Python installer
├── 🧹 clean.bat               # Cleanup utility
└── 📖 README.md               # This file
```

## ⚙️ Configuration

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--region` | `ap-northeast-1` | AWS region to analyze |
| `--days` | `30` | Analysis period in days |
| `--cpu-threshold` | `5.0` | CPU utilization threshold (%) |
| `--expensive-threshold` | `100.0` | Expensive instance threshold ($/month) |
| `--output` | None | JSON output file path |

### Direct Python Execution

If you prefer to run Python directly:

```bash
# Basic usage
python ec2_usage_analyzer.py

# With options
python ec2_usage_analyzer.py --region us-west-2 --days 7 --cpu-threshold 10.0

# Full configuration
python ec2_usage_analyzer.py --region ap-northeast-1 --days 14 --cpu-threshold 3.0 --expensive-threshold 150.0 --output report.json
```

## Sample Output

```
🚀 Starting AWS EC2 Cost Optimization Analysis
📍 Region: ap-northeast-1
📅 Analysis period: Last 30 days
🎯 CPU threshold: 5.0%
💰 Expensive threshold: $100/month

================================================================================
🔍 AWS EC2 Cost Optimization Analysis
================================================================================
📅 Analysis period: Last 30 days
🎯 CPU threshold: 5.0%
💰 Expensive instance threshold: $100/month
--------------------------------------------------------------------------------
[1/8] Analyzing: i-1234567890abcdef0 (web-server-prod) - m5.xlarge
[2/8] Analyzing: i-0987654321fedcba0 (database-server) - r5.2xlarge

====================================================================================================
💰 EC2 Cost Optimization Analysis Results
====================================================================================================
📊 Summary:
   Total running instances analyzed: 8
   Expensive long-running instances: 2
   Long-term running instances: 3
   Potential monthly savings: $245.50

🚨 HIGH PRIORITY: Expensive Long-Running Instances (24+ hours)
====================================================================================================
Instance ID          Name                 Type            Days     $/Month    CPU%     Current Cost Savings   
----------------------------------------------------------------------------------------------------
i-1234567890abcdef0  web-server-prod     m5.xlarge       45.2     $138       2.1%     $298.50      $149.25    
i-0987654321fedcba0  database-server     r5.2xlarge      72.1     $363       8.5%     $876.20      $0.00      

💡 Recommendations for expensive instances:
   - Review if these high-cost instances are still needed
   - Consider downsizing instances with low CPU utilization
   - Implement auto-shutdown schedules for development/testing instances
   - Consider Reserved Instances for long-term workloads

⚠️  MEDIUM PRIORITY: Long-Term Running Instances (30+ days)
====================================================================================================
Instance ID          Name                 Type            Days     $/Month    CPU%     Current Cost Savings   
----------------------------------------------------------------------------------------------------
i-abcdef1234567890   test-environment    t3.large        35.8     $60        1.2%     $71.50       $14.30     
i-fedcba0987654321   dev-server          t3.medium       42.3     $30        15.2%    $52.80       $0.00      
i-567890abcdef1234   backup-server       t3.small        67.2     $15        0.8%     $33.60       $6.72      

💡 Recommendations for long-term instances:
   - Review if continuous operation is necessary
   - Implement scheduled start/stop for non-production workloads
   - Consider spot instances for fault-tolerant workloads
   - Evaluate right-sizing opportunities

📄 Detailed report saved to cost_analysis.json
====================================================================================================
```

## Analysis Criteria

### Two-Tier Analysis Approach

#### 🚨 High Priority: Expensive Long-Running Instances
- **Criteria**: Monthly cost ≥ $100 AND running ≥ 24 hours
- **Focus**: High-cost instances that may benefit from immediate optimization
- **Potential Actions**: Downsizing, scheduling, Reserved Instances

#### ⚠️ Medium Priority: Long-Term Running Instances  
- **Criteria**: Running ≥ 30 days (regardless of cost)
- **Focus**: Instances that may have been forgotten or over-provisioned
- **Potential Actions**: Review necessity, implement scheduling, right-sizing

### Analysis Metrics
- **CPUUtilization**: Average CPU usage over analysis period
- **NetworkIn/NetworkOut**: Network traffic volume
- **Cost Calculation**: Based on current instance pricing (Tokyo region)
- **Potential Savings**: Estimated savings from optimization actions

### Excluded from Analysis
- **Stopped instances**: Not analyzed (no ongoing costs)
- **Recently launched**: Instances running < 24 hours (insufficient data)

## ⚠️ Important Notes

- **CloudWatch Costs**: This tool uses CloudWatch metrics which may incur charges
- **New Instances**: Instances running <24 hours may have insufficient metrics
- **Verification Required**: Always verify instance purpose before termination
- **Cost Estimates**: Pricing is approximate and based on Tokyo region rates

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Authentication Error** | Run `aws configure list` to verify credentials |
| **Permission Denied** | Ensure IAM user/role has required permissions |
| **Region Not Found** | Specify correct region with `--region` option |
| **Python Not Found** | Run `install_python.bat` as administrator |
| **Virtual Environment Issues** | Delete `venv` folder and re-run `setup.bat` |

### Getting Help

1. Check the [Issues](https://github.com/yoshitaka-atarashi/AWS-EC2CostAnalyzer/issues) page for known problems
2. Review AWS credentials and permissions
3. Ensure Python 3.7+ is installed
4. Verify network connectivity to AWS services

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yoshitaka-atarashi/AWS-EC2CostAnalyzer.git`
3. Run `setup.bat` to create development environment
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AWS SDK for Python (Boto3) team
- CloudWatch metrics service
- Open source community contributors

---

**⭐ If this tool helps you save costs, please consider giving it a star!**