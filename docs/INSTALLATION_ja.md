# インストールガイド

このガイドでは、AWS EC2コスト最適化アナライザーの詳細なインストール手順を説明します。

## 🚀 クイックインストール

### オプション1: ワンコマンドセットアップ（推奨）
```cmd
start.bat
```
これにより自動的に以下が実行されます：
- Pythonの検出またはインストール支援
- 仮想環境のセットアップ
- 依存関係のインストール
- アプリケーションの起動

### オプション2: 手動インストール

#### ステップ1: Pythonのインストール
Pythonがインストールされていない場合：
```cmd
install_python.bat
```
*管理者権限で実行*

#### ステップ2: 環境のセットアップ
```cmd
setup.bat
```

#### ステップ3: 分析の実行
```cmd
run.bat
```

## 📋 システム要件

### 最小要件
- **OS**: Windows 10 (1809+) または Windows 11
- **RAM**: 512 MB利用可能
- **ストレージ**: 100 MB空き容量
- **ネットワーク**: AWS API呼び出し用のインターネット接続

### 推奨要件
- **OS**: Windows 11 または Windows Server 2019+
- **RAM**: 2 GB利用可能
- **ストレージ**: 1 GB空き容量
- **Python**: 3.9+（必要に応じて自動インストール）

## 🔧 Pythonインストールオプション

### オプション1: Microsoft Store（推奨）
1. 管理者権限で`install_python.bat`を実行
2. オプション1を選択
3. Microsoft Storeからインストール
4. `setup.bat`を実行

### オプション2: 公式Python.org
1. https://python.org/downloads からダウンロード
2. **重要**: インストール時に「Add Python to PATH」をチェック
3. `setup.bat`を実行

### オプション3: Anaconda/Miniconda
1. AnacondaまたはMinicondaをインストール
2. ツールが自動的にインストールを検出
3. `setup.bat`を実行

## 🔐 AWS設定

### 方法1: AWS CLI（推奨）
```cmd
aws configure
```
以下を入力：
- AWS Access Key ID
- AWS Secret Access Key
- デフォルトリージョン（例：ap-northeast-1）
- 出力形式（json）

### 方法2: 環境変数
```cmd
set AWS_ACCESS_KEY_ID=your_access_key_here
set AWS_SECRET_ACCESS_KEY=your_secret_key_here
set AWS_DEFAULT_REGION=ap-northeast-1
```

### 方法3: IAMロール（EC2インスタンスのみ）
EC2上で実行する場合、必要な権限を持つIAMロールをアタッチします。

## 🛡️ 必要なIAM権限

以下の権限でIAMポリシーを作成：
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

## 🔍 検証

### インストールのテスト
```cmd
run.bat --help
```

### AWS接続のテスト
```cmd
aws sts get-caller-identity
```

## 🐛 トラブルシューティング

### Python関連の問題
| 問題 | 解決方法 |
|------|----------|
| "Python not found" | 管理者権限で`install_python.bat`を実行 |
| "Permission denied" | Windows実行ポリシーを確認 |
| "Module not found" | `venv`フォルダを削除して`setup.bat`を再実行 |

### AWS関連の問題
| 問題 | 解決方法 |
|------|----------|
| "Credentials not found" | `aws configure`を実行または環境変数を設定 |
| "Access denied" | IAM権限を確認 |
| "Region not found" | 有効なリージョンで`--region`パラメータを使用 |

### Windows関連の問題
| 問題 | 解決方法 |
|------|----------|
| "Execution policy" | PowerShellで`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`を実行 |
| "Character encoding" | すべてのスクリプトはUTF-8を使用、最新のWindowsで動作するはず |
| "Antivirus blocking" | プロジェクトフォルダをアンチウイルスの除外に追加 |

## 🔄 更新

### ツールの更新
```cmd
git pull origin main
setup.bat
```

### 依存関係のみ更新
```cmd
venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

## 🧹 アンインストール

### 仮想環境の削除
```cmd
clean.bat
```

### 完全削除
1. `clean.bat`を実行
2. プロジェクトフォルダを削除
3. 作成したショートカットを削除

## 📞 ヘルプの取得

問題が発生した場合：
1. このトラブルシューティングガイドを確認
2. メインの[README_ja.md](../README_ja.md)を確認
3. 既存の[GitHub Issues](https://github.com/yoshitaka-atarashi/AWS-EC2CostAnalyzer/issues)を検索
4. 詳細情報を含む新しいIssueを作成

## 🎯 次のステップ

インストール後：
1. [使用ガイド](../README_ja.md#使用方法)を確認
2. `run.bat`で最初の分析を実行
3. `run_with_options.bat`で対話モードを試す
4. 高度な設定オプションを確認