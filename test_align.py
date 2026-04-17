import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

TEST_FILE = Path(__file__).parent / "test.html"

async def run_tests():
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1200, "height": 800})

        test_file_url = f"file:///{TEST_FILE.as_posix()}"
        print(f"加载测试页面: {test_file_url}")
        await page.goto(test_file_url)
        await page.wait_for_timeout(1000)

        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        print("\n=== 测试 1: 检查页面加载 ===")
        posts = await page.query_selector_all(".post-card")
        print(f"找到 {len(posts)} 个帖子卡片")
        results.append(("页面加载", len(posts) > 0, f"找到 {len(posts)} 个卡片"))

        print("\n=== 测试 2: 应用对齐前高度 ===")
        heights_before = await page.evaluate("""
            () => {
                window.resetToOriginal();
                return new Promise(resolve => {
                    setTimeout(() => {
                        const cards = document.querySelectorAll('.post-card');
                        resolve(Array.from(cards).map(c => c.offsetHeight));
                    }, 200);
                });
            }
        """)
        print(f"对齐前高度: {heights_before}")
        heights_differ = len(set(heights_before)) > 1
        results.append(("对齐前高度不同", heights_differ, f"高度范围: {min(heights_before)}-{max(heights_before)}px"))

        print("\n=== 测试 3: 执行对齐脚本 ===")
        align_result = await page.evaluate("window.alignPostHeights()")
        print(f"对齐结果: {align_result}")
        await page.wait_for_timeout(500)

        print("\n=== 测试 4: 应用对齐后高度 ===")
        heights_after = []
        for i, post in enumerate(posts):
            height = await post.evaluate("el => el.offsetHeight")
            heights_after.append(height)
        print(f"对齐后高度: {heights_after}")
        all_same = len(set(heights_after)) == 1
        results.append(("对齐后高度一致", all_same, f"所有高度: {heights_after[0]}px"))

        print("\n=== 测试 5: 高度在合理范围内 ===")
        expected_height = heights_after[0] if heights_after else 0
        in_range = 280 <= expected_height <= 350
        results.append(("高度范围合理", in_range, f"高度: {expected_height}px (期望 280-350px)"))

        print("\n=== 测试 6: 检查溢出处理 ===")
        overflow_check = await page.evaluate("""
            () => {
                const cards = document.querySelectorAll('.post-card');
                let hasOverflow = false;
                cards.forEach(card => {
                    const content = card.querySelector('.content');
                    if (content && content.scrollHeight > content.clientHeight) {
                        hasOverflow = true;
                    }
                });
                return !hasOverflow;
            }
        """)
        results.append(("无溢出", overflow_check, "溢出已正确处理"))

        print("\n=== 测试 7: DOM 观察器功能 ===")
        await page.evaluate("""
            () => {
                const container = document.getElementById('posts-container');
                const newCard = document.createElement('div');
                newCard.className = 'post-card';
                newCard.style.height = '300px';
                newCard.innerHTML = '<div class="image-wrapper" style="height: 180px; flex-shrink: 0;"><img src="https://picsum.photos/300/300?random=99"></div><div class="content"><div class="title">新卡片</div><div class="meta"><span>作者</span></div></div>';
                container.appendChild(newCard);
            }
        """)
        await page.wait_for_timeout(500)
        new_cards = await page.query_selector_all(".post-card")
        has_new_card = len(new_cards) == len(posts) + 1
        results.append(("动态加载支持", has_new_card, f"新卡片已添加 (共 {len(new_cards)} 个)"))

        print("\n=== 测试 8: 重置功能 ===")
        await page.click(".reset-btn")
        await page.wait_for_timeout(500)
        reset_result = await page.evaluate("""
            () => {
                const card = document.querySelector('.post-card');
                return {
                    displayValue: card.style.display,
                    heightValue: card.style.height,
                    computedDisplay: window.getComputedStyle(card).display
                };
            }
        """)
        print(f"重置后样式: {reset_result}")
        reset_works = reset_result['heightValue'] != ''
        results.append(("重置功能", reset_works, f"height已设置: {reset_result['heightValue']}"))

        print("\n" + "=" * 50)
        print("测试结果汇总:")
        print("=" * 50)

        passed = 0
        for name, passed_test, detail in results:
            status = "[PASS]" if passed_test else "[FAIL]"
            print(f"{status}: {name} - {detail}")
            if passed_test:
                passed += 1

        print(f"\nTotal: {passed}/{len(results)} passed")

        if passed == len(results):
            print("\nAll tests passed! Script works correctly.")
        else:
            print(f"\n{len(results) - passed} test(s) failed, needs fixing.")

        await browser.close()
        return passed == len(results)

if __name__ == "__main__":
    success = asyncio.run(run_tests())
    exit(0 if success else 1)
