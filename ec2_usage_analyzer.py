#!/usr/bin/env python3
"""
AWS EC2使用状況分析ツール
長期間使用されていないEC2インスタンスを特定します
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import argparse

class EC2UsageAnalyzer:
    def __init__(self, region_name: str = 'ap-northeast-1'):
        """
        EC2使用状況分析クラスの初期化
        
        Args:
            region_name: AWSリージョン名（デフォルト: ap-northeast-1）
        """
        self.ec2_client = boto3.client('ec2', region_name=region_name)
        self.cloudwatch_client = boto3.client('cloudwatch', region_name=region_name)
        self.region_name = region_name
    
    def get_all_instances(self) -> List[Dict[str, Any]]:
        """
        全てのEC2インスタンス情報を取得
        
        Returns:
            インスタンス情報のリスト
        """
        try:
            response = self.ec2_client.describe_instances()
            instances = []
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    # インスタンス名を取得
                    name = 'N/A'
                    if 'Tags' in instance:
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Name':
                                name = tag['Value']
                                break
                    
                    instance_info = {
                        'InstanceId': instance['InstanceId'],
                        'Name': name,
                        'State': instance['State']['Name'],
                        'InstanceType': instance['InstanceType'],
                        'LaunchTime': instance['LaunchTime'],
                        'Platform': instance.get('Platform', 'Linux'),
                        'VpcId': instance.get('VpcId', 'N/A'),
                        'SubnetId': instance.get('SubnetId', 'N/A')
                    }
                    instances.append(instance_info)
            
            return instances
        except Exception as e:
            print(f"インスタンス情報の取得に失敗しました: {e}")
            return []
    def get_cpu_utilization(self, instance_id: str, days: int = 30) -> float:
        """
        指定期間のCPU使用率平均を取得
        
        Args:
            instance_id: インスタンスID
            days: 確認する日数（デフォルト: 30日）
            
        Returns:
            CPU使用率の平均値
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            response = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,  # 1日
                Statistics=['Average']
            )
            
            if response['Datapoints']:
                avg_cpu = sum(point['Average'] for point in response['Datapoints']) / len(response['Datapoints'])
                return round(avg_cpu, 2)
            else:
                return 0.0
                
        except Exception as e:
            print(f"CPU使用率の取得に失敗しました ({instance_id}): {e}")
            return -1.0
    
    def get_network_activity(self, instance_id: str, days: int = 30) -> Dict[str, float]:
        """
        指定期間のネットワーク活動を取得
        
        Args:
            instance_id: インスタンスID
            days: 確認する日数
            
        Returns:
            ネットワークIn/Outの合計値
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            # NetworkIn
            response_in = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='NetworkIn',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=['Sum']
            )
            
            # NetworkOut
            response_out = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='NetworkOut',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=['Sum']
            )
            
            network_in = sum(point['Sum'] for point in response_in['Datapoints']) if response_in['Datapoints'] else 0
            network_out = sum(point['Sum'] for point in response_out['Datapoints']) if response_out['Datapoints'] else 0
            
            return {
                'NetworkIn': round(network_in / (1024**3), 2),  # GB単位
                'NetworkOut': round(network_out / (1024**3), 2)  # GB単位
            }
            
        except Exception as e:
            print(f"ネットワーク活動の取得に失敗しました ({instance_id}): {e}")
            return {'NetworkIn': -1, 'NetworkOut': -1}
    def get_instance_cost_info(self, instance_type: str) -> Dict[str, float]:
        """
        インスタンスタイプの概算コスト情報を取得
        
        Args:
            instance_type: EC2インスタンスタイプ
            
        Returns:
            時間単価と月額概算のディクショナリ
        """
        # 主要なインスタンスタイプの概算料金（東京リージョン、USD/hour）
        # 実際の料金は変動するため、参考値として使用
        cost_map = {
            # General Purpose
            't3.nano': 0.0052, 't3.micro': 0.0104, 't3.small': 0.0208, 't3.medium': 0.0416,
            't3.large': 0.0832, 't3.xlarge': 0.1664, 't3.2xlarge': 0.3328,
            't2.nano': 0.0058, 't2.micro': 0.0116, 't2.small': 0.023, 't2.medium': 0.046,
            't2.large': 0.092, 't2.xlarge': 0.184, 't2.2xlarge': 0.368,
            'm5.large': 0.096, 'm5.xlarge': 0.192, 'm5.2xlarge': 0.384, 'm5.4xlarge': 0.768,
            'm5.8xlarge': 1.536, 'm5.12xlarge': 2.304, 'm5.16xlarge': 3.072, 'm5.24xlarge': 4.608,
            'm6i.large': 0.0864, 'm6i.xlarge': 0.1728, 'm6i.2xlarge': 0.3456, 'm6i.4xlarge': 0.6912,
            
            # Compute Optimized
            'c5.large': 0.085, 'c5.xlarge': 0.17, 'c5.2xlarge': 0.34, 'c5.4xlarge': 0.68,
            'c5.9xlarge': 1.53, 'c5.12xlarge': 2.04, 'c5.18xlarge': 3.06, 'c5.24xlarge': 4.08,
            'c6i.large': 0.0765, 'c6i.xlarge': 0.153, 'c6i.2xlarge': 0.306, 'c6i.4xlarge': 0.612,
            
            # Memory Optimized
            'r5.large': 0.126, 'r5.xlarge': 0.252, 'r5.2xlarge': 0.504, 'r5.4xlarge': 1.008,
            'r5.8xlarge': 2.016, 'r5.12xlarge': 3.024, 'r5.16xlarge': 4.032, 'r5.24xlarge': 6.048,
            
            # Storage Optimized
            'i3.large': 0.156, 'i3.xlarge': 0.312, 'i3.2xlarge': 0.624, 'i3.4xlarge': 1.248,
            'i3.8xlarge': 2.496, 'i3.16xlarge': 4.992,
        }
        
        hourly_cost = cost_map.get(instance_type, 0.1)  # デフォルト値
        monthly_cost = hourly_cost * 24 * 30  # 月額概算
        
        return {
            'hourly_cost': hourly_cost,
            'monthly_cost': monthly_cost
        }
    
    def is_expensive_instance(self, instance_type: str, threshold_monthly: float = 100.0) -> bool:
        """
        高額インスタンスかどうかを判定
        
        Args:
            instance_type: インスタンスタイプ
            threshold_monthly: 月額閾値（USD）
            
        Returns:
            高額インスタンスの場合True
        """
        cost_info = self.get_instance_cost_info(instance_type)
        return cost_info['monthly_cost'] >= threshold_monthly
    
    def analyze_cost_optimization(self, cpu_threshold: float = 5.0, days: int = 30, 
                                expensive_threshold: float = 100.0) -> Dict[str, List[Dict[str, Any]]]:
        """
        コスト最適化の観点でEC2インスタンスを分析
        
        Args:
            cpu_threshold: CPU使用率の閾値（％）
            days: 分析期間（日）
            expensive_threshold: 高額インスタンスの月額閾値（USD）
            
        Returns:
            分析結果のディクショナリ
        """
        print("=" * 80)
        print("🔍 AWS EC2 Cost Optimization Analysis")
        print("=" * 80)
        print(f"📅 Analysis period: Last {days} days")
        print(f"🎯 CPU threshold: {cpu_threshold}%")
        print(f"💰 Expensive instance threshold: ${expensive_threshold}/month")
        print("-" * 80)
        
        instances = self.get_all_instances()
        
        # 分析結果を格納する辞書
        results = {
            'expensive_long_running': [],  # 高額で長時間稼働
            'long_term_running': [],       # 長期間稼働
            'summary': {}
        }
        
        expensive_count = 0
        long_term_count = 0
        total_potential_savings = 0
        
        for i, instance in enumerate(instances, 1):
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            
            # 停止中のインスタンスはスキップ
            if instance['State'] != 'running':
                continue
                
            print(f"[{i}/{len(instances)}] Analyzing: {instance_id} ({instance['Name']}) - {instance_type}")
            
            launch_time = instance['LaunchTime'].replace(tzinfo=None)
            hours_running = (datetime.utcnow() - launch_time).total_seconds() / 3600
            days_running = hours_running / 24
            
            cost_info = self.get_instance_cost_info(instance_type)
            is_expensive = self.is_expensive_instance(instance_type, expensive_threshold)
            
            # CPU使用率とネットワーク活動を取得
            cpu_avg = self.get_cpu_utilization(instance_id, min(days, int(days_running)))
            network_stats = self.get_network_activity(instance_id, min(days, int(days_running)))
            
            # 現在のコスト計算
            current_cost = cost_info['hourly_cost'] * hours_running
            
            instance_data = {
                'InstanceId': instance_id,
                'Name': instance['Name'],
                'InstanceType': instance_type,
                'State': instance['State'],
                'LaunchTime': launch_time.strftime('%Y-%m-%d %H:%M:%S'),
                'HoursRunning': round(hours_running, 1),
                'DaysRunning': round(days_running, 1),
                'HourlyCost': cost_info['hourly_cost'],
                'MonthlyCost': cost_info['monthly_cost'],
                'CurrentCost': round(current_cost, 2),
                'AvgCPU': cpu_avg if cpu_avg >= 0 else 'N/A',
                'NetworkIn': network_stats['NetworkIn'],
                'NetworkOut': network_stats['NetworkOut'],
                'IsExpensive': is_expensive,
                'LowUtilization': cpu_avg >= 0 and cpu_avg < cpu_threshold
            }
            
            # 1. 高額インスタンスで24時間以上稼働している場合
            if is_expensive and hours_running >= 24:
                reason = f"Expensive instance (${cost_info['monthly_cost']:.0f}/month) running for {days_running:.1f} days"
                if cpu_avg >= 0 and cpu_avg < cpu_threshold:
                    reason += f" with low CPU usage ({cpu_avg}%)"
                    # 潜在的な節約額を計算（より小さなインスタンスに変更した場合）
                    potential_savings = current_cost * 0.5  # 50%の節約を仮定
                    total_potential_savings += potential_savings
                    instance_data['PotentialSavings'] = round(potential_savings, 2)
                
                instance_data['Reason'] = reason
                results['expensive_long_running'].append(instance_data)
                expensive_count += 1
            
            # 2. 1ヶ月以上稼働している場合（高額でない場合も含む）
            elif days_running >= 30:
                reason = f"Long-term running ({days_running:.1f} days)"
                if cpu_avg >= 0 and cpu_avg < cpu_threshold:
                    reason += f" with low CPU usage ({cpu_avg}%)"
                    # 停止による節約額を計算
                    potential_savings = cost_info['hourly_cost'] * 24 * 7  # 1週間停止した場合
                    total_potential_savings += potential_savings
                    instance_data['PotentialSavings'] = round(potential_savings, 2)
                
                instance_data['Reason'] = reason
                results['long_term_running'].append(instance_data)
                long_term_count += 1
        
        # サマリー情報
        results['summary'] = {
            'total_instances_analyzed': len([i for i in instances if i['State'] == 'running']),
            'expensive_long_running_count': expensive_count,
            'long_term_running_count': long_term_count,
            'total_potential_savings': round(total_potential_savings, 2)
        }
        
        return results
    
    def generate_cost_report(self, analysis_results: Dict[str, Any], output_file: str = None):
        """
        コスト最適化分析結果のレポートを生成
        
        Args:
            analysis_results: 分析結果のディクショナリ
            output_file: 出力ファイル名（オプション）
        """
        print("\n" + "=" * 100)
        print("💰 EC2 Cost Optimization Analysis Results")
        print("=" * 100)
        
        summary = analysis_results['summary']
        expensive_instances = analysis_results['expensive_long_running']
        long_term_instances = analysis_results['long_term_running']
        
        # サマリー表示
        print(f"📊 Summary:")
        print(f"   Total running instances analyzed: {summary['total_instances_analyzed']}")
        print(f"   Expensive long-running instances: {summary['expensive_long_running_count']}")
        print(f"   Long-term running instances: {summary['long_term_running_count']}")
        print(f"   Potential monthly savings: ${summary['total_potential_savings']:.2f}")
        print()
        
        # 1. 高額で長時間稼働しているインスタンス
        if expensive_instances:
            print("🚨 HIGH PRIORITY: Expensive Long-Running Instances (24+ hours)")
            print("=" * 100)
            header = f"{'Instance ID':<20} {'Name':<20} {'Type':<15} {'Days':<8} {'$/Month':<10} {'CPU%':<8} {'Current Cost':<12} {'Savings':<10}"
            print(header)
            print("-" * len(header))
            
            for instance in expensive_instances:
                savings = instance.get('PotentialSavings', 0)
                cpu_display = f"{instance['AvgCPU']}%" if isinstance(instance['AvgCPU'], (int, float)) else str(instance['AvgCPU'])
                
                print(f"{instance['InstanceId']:<20} {instance['Name'][:19]:<20} {instance['InstanceType']:<15} "
                      f"{instance['DaysRunning']:<8.1f} ${instance['MonthlyCost']:<9.0f} {cpu_display:<8} "
                      f"${instance['CurrentCost']:<11.2f} ${savings:<9.2f}")
            
            print(f"\n💡 Recommendations for expensive instances:")
            print("   - Review if these high-cost instances are still needed")
            print("   - Consider downsizing instances with low CPU utilization")
            print("   - Implement auto-shutdown schedules for development/testing instances")
            print("   - Consider Reserved Instances for long-term workloads")
            print()
        
        # 2. 長期間稼働しているインスタンス
        if long_term_instances:
            print("⚠️  MEDIUM PRIORITY: Long-Term Running Instances (30+ days)")
            print("=" * 100)
            header = f"{'Instance ID':<20} {'Name':<20} {'Type':<15} {'Days':<8} {'$/Month':<10} {'CPU%':<8} {'Current Cost':<12} {'Savings':<10}"
            print(header)
            print("-" * len(header))
            
            for instance in long_term_instances:
                savings = instance.get('PotentialSavings', 0)
                cpu_display = f"{instance['AvgCPU']}%" if isinstance(instance['AvgCPU'], (int, float)) else str(instance['AvgCPU'])
                
                print(f"{instance['InstanceId']:<20} {instance['Name'][:19]:<20} {instance['InstanceType']:<15} "
                      f"{instance['DaysRunning']:<8.1f} ${instance['MonthlyCost']:<9.0f} {cpu_display:<8} "
                      f"${instance['CurrentCost']:<11.2f} ${savings:<9.2f}")
            
            print(f"\n💡 Recommendations for long-term instances:")
            print("   - Review if continuous operation is necessary")
            print("   - Implement scheduled start/stop for non-production workloads")
            print("   - Consider spot instances for fault-tolerant workloads")
            print("   - Evaluate right-sizing opportunities")
            print()
        
        if not expensive_instances and not long_term_instances:
            print("✅ No cost optimization opportunities found based on current criteria.")
            print("   All running instances appear to be appropriately sized and utilized.")
            print()
        
        # JSONファイルとして保存
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, ensure_ascii=False, indent=2, default=str)
            print(f"📄 Detailed report saved to {output_file}")
        
        print("=" * 100)
def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='AWS EC2 Cost Optimization Analyzer')
    parser.add_argument('--region', default='ap-northeast-1', help='AWS region (default: ap-northeast-1)')
    parser.add_argument('--days', type=int, default=30, help='Analysis period in days (default: 30)')
    parser.add_argument('--cpu-threshold', type=float, default=5.0, help='CPU utilization threshold %% (default: 5.0)')
    parser.add_argument('--expensive-threshold', type=float, default=100.0, help='Expensive instance monthly cost threshold USD (default: 100.0)')
    parser.add_argument('--output', help='Output results to JSON file')
    
    args = parser.parse_args()
    
    print("🚀 Starting AWS EC2 Cost Optimization Analysis")
    print(f"📍 Region: {args.region}")
    print(f"📅 Analysis period: Last {args.days} days")
    print(f"🎯 CPU threshold: {args.cpu_threshold}%")
    print(f"💰 Expensive threshold: ${args.expensive_threshold}/month")
    print()
    
    try:
        # Execute analysis
        analyzer = EC2UsageAnalyzer(region_name=args.region)
        analysis_results = analyzer.analyze_cost_optimization(
            cpu_threshold=args.cpu_threshold,
            days=args.days,
            expensive_threshold=args.expensive_threshold
        )
        
        # Generate report
        analyzer.generate_cost_report(analysis_results, args.output)
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("Please check your AWS credentials and region settings.")

if __name__ == "__main__":
    main()