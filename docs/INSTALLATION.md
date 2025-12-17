# Installation Guide

This guide provides detailed installation instructions for the AWS EC2 Cost Analyzer.

## 🚀 Quick Installation

### Option 1: One-Command Setup (Recommended)
```cmd
start.bat
```
This will automatically:
- Detect or help install Python
- Set up virtual environment
- Install dependencies
- Launch the application

### Option 2: Manual Installation

#### Step 1: Install Python
If Python is not installed:
```cmd
install_python.bat
```
*Run as administrator*

#### Step 2: Set up Environment
```cmd
setup.bat
```

#### Step 3: Run Analysis
```cmd
run.bat
```

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10 (1809+) or Windows 11
- **RAM**: 512 MB available
- **Storage**: 100 MB free space
- **Network**: Internet connection for AWS API calls

### Recommended Requirements
- **OS**: Windows 11 or Windows Server 2019+
- **RAM**: 2 GB available
- **Storage**: 1 GB free space
- **Python**: 3.9+ (automatically installed if needed)

## 🔧 Python Installation Options

### Option 1: Microsoft Store (Recommended)
1. Run `install_python.bat` as administrator
2. Select option 1
3. Install from Microsoft Store
4. Run `setup.bat`

### Option 2: Official Python.org
1. Download from https://python.org/downloads
2. **Important**: Check "Add Python to PATH" during installation
3. Run `setup.bat`

### Option 3: Anaconda/Miniconda
1. Install Anaconda or Miniconda
2. The tool will auto-detect your installation
3. Run `setup.bat`

## 🔐 AWS Configuration

### Method 1: AWS CLI (Recommended)
```cmd
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., ap-northeast-1)
- Output format (json)

### Method 2: Environment Variables
```cmd
set AWS_ACCESS_KEY_ID=your_access_key_here
set AWS_SECRET_ACCESS_KEY=your_secret_key_here
set AWS_DEFAULT_REGION=ap-northeast-1
```

### Method 3: IAM Role (EC2 instances only)
If running on EC2, attach an IAM role with required permissions.

## 🛡️ Required IAM Permissions

Create an IAM policy with these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "cloudwatch:GetMetricStatistics"
            ],
            "Resource": "*"
        }
    ]
}
```

## 🔍 Verification

### Test Installation
```cmd
run.bat --help
```

### Test AWS Connection
```cmd
aws sts get-caller-identity
```

## 🐛 Troubleshooting

### Python Issues
| Problem | Solution |
|---------|----------|
| "Python not found" | Run `install_python.bat` as administrator |
| "Permission denied" | Check Windows execution policy |
| "Module not found" | Delete `venv` folder and re-run `setup.bat` |

### AWS Issues
| Problem | Solution |
|---------|----------|
| "Credentials not found" | Run `aws configure` or set environment variables |
| "Access denied" | Check IAM permissions |
| "Region not found" | Use `--region` parameter with valid region |

### Windows Issues
| Problem | Solution |
|---------|----------|
| "Execution policy" | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell |
| "Character encoding" | All scripts use UTF-8, should work on modern Windows |
| "Antivirus blocking" | Add project folder to antivirus exclusions |

## 🔄 Updating

### Update the Tool
```cmd
git pull origin main
setup.bat
```

### Update Dependencies Only
```cmd
venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

## 🧹 Uninstallation

### Remove Virtual Environment
```cmd
clean.bat
```

### Complete Removal
1. Run `clean.bat`
2. Delete the project folder
3. Remove any shortcuts created

## 📞 Getting Help

If you encounter issues:
1. Check this troubleshooting guide
2. Review the main [README.md](../README.md)
3. Search existing [GitHub Issues](https://github.com/your-repo/issues)
4. Create a new issue with detailed information

## 🎯 Next Steps

After installation:
1. Review the [Usage Guide](../README.md#usage)
2. Run your first analysis with `run.bat`
3. Explore interactive mode with `run_with_options.bat`
4. Check out advanced configuration options