#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可转债申购查询脚本
功能：查询今日/明日可申购的新债信息，并通过 Server酱 推送到微信
"""

import argparse
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sys
import os

# 添加父目录到路径以便导入 utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import akshare as ak
    from dateutil import parser as date_parser
except ImportError as e:
    print(f"❌ 缺少依赖库: {str(e)}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)


class BondMonitor:
    """可转债监控类"""
    
    def __init__(self, sendkey: str, send_daily_status: bool = False):
        """
        初始化监控器
        
        Args:
            sendkey: Server酱 SendKey
            send_daily_status: 是否发送每日状态通知
        """
        self.sendkey = sendkey
        self.send_daily_status = send_daily_status
        self.serverchan_url = f"https://sctapi.ftqq.com/{sendkey}.send"
        
    def get_bond_data(self) -> Optional[List[Dict]]:
        """
        获取可转债数据
        
        Returns:
            可转债数据列表，失败返回 None
        """
        try:
            print("🔄 正在获取可转债数据...")
            df = ak.bond_zh_cov()
            
            if df is None or df.empty:
                print("❌ 未获取到数据")
                return None
            
            # 转换为字典列表
            bonds = df.to_dict('records')
            print(f"✅ 成功获取 {len(bonds)} 条债券数据")
            
            return bonds
            
        except Exception as e:
            print(f"❌ 获取数据失败: {str(e)}")
            return None
    
    def filter_new_bonds(self, bonds: List[Dict]) -> Dict[str, List[Dict]]:
        """
        筛选今日和明日的可申购新债
        
        Args:
            bonds: 可转债数据列表
            
        Returns:
            包含 'today' 和 'tomorrow' 键的字典
        """
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        result = {
            'today': [],
            'tomorrow': []
        }
        
        for bond in bonds:
            try:
                # 解析申购日期（字段名可能是 '申购日期' 或 'ISSUE_DT'）
                date_str = bond.get('申购日期') or bond.get('ISSUE_DT')
                if not date_str:
                    continue
                
                # 解析日期
                issue_date = date_parser.parse(str(date_str)).date()
                
                # 筛选今日和明日
                if issue_date == today:
                    result['today'].append(bond)
                elif issue_date == tomorrow:
                    result['tomorrow'].append(bond)
                    
            except Exception as e:
                # 日期解析失败，跳过
                continue
        
        return result
    
    def format_bond_info(self, bond: Dict) -> str:
        """
        格式化单个债券信息
        
        Args:
            bond: 债券数据字典
            
        Returns:
            格式化的字符串
        """
        name = bond.get('债券简称') or bond.get('BOND_ABBR') or '未知'
        code = bond.get('债券代码') or bond.get('BOND_CODE') or '未知'
        issue_date = bond.get('申购日期') or bond.get('ISSUE_DT') or '未知'
        
        # 尝试获取转股价值和发行规模
        convert_value = bond.get('转股价值') or bond.get('CONVERT_VALUE') or '未知'
        issue_size = bond.get('发行规模') or bond.get('ISSUE_SIZE') or '未知'
        
        info = f"{name}（{code}）\n"
        info += f"   - 申购日期：{issue_date}\n"
        info += f"   - 转股价值：{convert_value}\n"
        info += f"   - 发行规模：{issue_size}亿"
        
        return info
    
    def format_push_message(self, filtered_bonds: Dict[str, List[Dict]]) -> str:
        """
        格式化推送消息
        
        Args:
            filtered_bonds: 筛选后的债券数据
            
        Returns:
            格式化的消息文本
        """
        today_count = len(filtered_bonds['today'])
        tomorrow_count = len(filtered_bonds['tomorrow'])
        
        # 如果没有新债且未启用每日状态
        if today_count == 0 and tomorrow_count == 0 and not self.send_daily_status:
            return ""
        
        message = "🔔 可转债申购提醒\n\n"
        
        # 今日新债
        if today_count > 0:
            message += f"📅 今日可申购（{today_count}只）：\n"
            for i, bond in enumerate(filtered_bonds['today'], 1):
                message += f"{i}. {self.format_bond_info(bond)}\n"
            message += "\n"
        
        # 明日新债
        if tomorrow_count > 0:
            message += f"📅 明日可申购（{tomorrow_count}只）：\n"
            for i, bond in enumerate(filtered_bonds['tomorrow'], 1):
                message += f"{i}. {self.format_bond_info(bond)}\n"
            message += "\n"
        
        # 无新债提醒
        if today_count == 0 and tomorrow_count == 0:
            message += "📭 今日无新债申购\n"
            message += "明日也无新债申购\n\n"
        
        message += "💡 提示：请提前准备申购资金"
        
        return message
    
    def push_to_wechat(self, title: str, message: str) -> bool:
        """
        推送到微信
        
        Args:
            title: 消息标题
            message: 消息内容
            
        Returns:
            是否成功
        """
        try:
            print("📤 正在推送消息到微信...")
            
            payload = {
                'title': title,
                'desp': message
            }
            
            response = requests.post(
                self.serverchan_url,
                data=payload,
                timeout=10
            )
            
            result = response.json()
            
            if result.get('code') == 0:
                print(f"✅ 推送成功: {title}")
                return True
            else:
                print(f"❌ 推送失败: {result.get('message', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"❌ 推送失败: {str(e)}")
            return False
    
    def run(self) -> bool:
        """
        执行监控任务
        
        Returns:
            是否成功
        """
        print("=" * 60)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔔 可转债申购监控启动")
        print("=" * 60)
        print()
        
        # 获取数据
        bonds = self.get_bond_data()
        if bonds is None:
            return False
        
        # 筛选新债
        filtered_bonds = self.filter_new_bonds(bonds)
        today_count = len(filtered_bonds['today'])
        tomorrow_count = len(filtered_bonds['tomorrow'])
        
        print(f"📊 筛选出 {today_count} 只今日新债，{tomorrow_count} 只明日新债")
        
        # 格式化消息
        message = self.format_push_message(filtered_bonds)
        
        if not message:
            print("ℹ️  今日无新债申购，且未启用每日状态通知，跳过推送")
            return True
        
        # 确定标题
        if today_count > 0:
            title = f"今日有{today_count}只新债申购"
        elif tomorrow_count > 0:
            title = f"明日有{tomorrow_count}只新债申购"
        else:
            title = "今日无新债申购"
        
        # 推送消息
        success = self.push_to_wechat(title, message)
        
        print()
        print("=" * 60)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 监控任务完成")
        print("=" * 60)
        
        return success


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='可转债申购查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础查询并推送
  python query_bond.py --sendkey YOUR_SENDKEY
  
  # 启用每日状态通知
  python query_bond.py --sendkey YOUR_SENDKEY --daily-status
  
  # 不推送，仅查看
  python query_bond.py --sendkey YOUR_SENDKEY --dry-run
        """
    )
    
    parser.add_argument(
        '--sendkey',
        required=True,
        help='Server酱 SendKey（必需）'
    )
    
    parser.add_argument(
        '--daily-status',
        action='store_true',
        help='发送每日状态通知（即使没有新债）'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅查询不推送（测试模式）'
    )
    
    args = parser.parse_args()
    
    # 创建监控器
    monitor = BondMonitor(
        sendkey=args.sendkey,
        send_daily_status=args.daily_status
    )
    
    # 测试模式
    if args.dry_run:
        print("🧪 测试模式：仅查询不推送\n")
        bonds = monitor.get_bond_data()
        if bonds:
            filtered = monitor.filter_new_bonds(bonds)
            print(f"\n📊 查询结果：")
            print(f"  - 今日可申购：{len(filtered['today'])} 只")
            print(f"  - 明日可申购：{len(filtered['tomorrow'])} 只")
            
            if filtered['today']:
                print("\n今日新债：")
                for bond in filtered['today']:
                    print(f"  - {monitor.format_bond_info(bond)}")
            
            if filtered['tomorrow']:
                print("\n明日新债：")
                for bond in filtered['tomorrow']:
                    print(f"  - {monitor.format_bond_info(bond)}")
        return
    
    # 执行监控
    success = monitor.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
