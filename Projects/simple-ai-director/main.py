"""
Simple AI Director - 命令行入口
"""

import sys
import os


def main():
    """命令行入口"""
    # 确保可以导入本地模块
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from core.director import AIDirector

    print("🎬 Simple AI Director - 创意导演助手")
    print("=" * 50)
    print("输入 'quit' 或 'exit' 退出\n")

    try:
        director = AIDirector()

        while True:
            user_input = input("你的创意: ").strip()

            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n感谢使用 Simple AI Director! 再见!")
                break

            if not user_input:
                continue

            if user_input.lower() == 'stats':
                stats = director.get_session_stats()
                print("\n会话统计:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                print()
                continue

            print("\n林导: ", end="", flush=True)
            response = director.chat(user_input)
            print(response)
            print()

    except KeyboardInterrupt:
        print("\n\n感谢使用 Simple AI Director! 再见!")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
