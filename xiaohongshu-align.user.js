// ==UserScript==
// @name         小红书首页帖子对齐
// @namespace    http://tampermonkey.net/
// @version      1.5
// @description   统一小红书首页帖子卡片高度使其左右对齐
// @author       You
// @match        https://www.xiaohongshu.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const CONFIG = {
        cardSelector: 'a[href*="/explore/"]',
        footerSelector: 'a[href*="/explore/"] + div.footer, div.footer',
        targetHeight: 300
    };

    const addGlobalStyle = () => {
        let style = document.getElementById('xhs-align-styles');
        if (!style) {
            style = document.createElement('style');
            style.id = 'xhs-align-styles';
            document.head.appendChild(style);
        }
        style.textContent = `
            a[href*="/explore/"] {
                height: ${CONFIG.targetHeight}px !important;
                flex-shrink: 0 !important;
            }
            div.footer {
                position: absolute !important;
                bottom: 0 !important;
                left: 0 !important;
                right: 0 !important;
                height: auto !important;
                max-height: ${CONFIG.targetHeight * 0.4}px !important;
                padding: 8px !important;
                box-sizing: border-box !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: flex-end !important;
                background: linear-gradient(transparent, rgba(0,0,0,0.5)) !important;
            }
            div.footer .title {
                height: auto !important;
                max-height: 40px !important;
                overflow: hidden !important;
                display: -webkit-box !important;
                -webkit-line-clamp: 2 !important;
                -webkit-box-orient: vertical !important;
                color: #fff !important;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.8), 0 0 10px rgba(0,0,0,0.5) !important;
            }
            div.footer .author-wrapper {
                text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
            }
        `;
    };

    const alignPostHeights = () => {
        const cards = document.querySelectorAll(CONFIG.cardSelector);
        if (cards.length === 0) return;

        cards.forEach(card => {
            card.style.setProperty('height', CONFIG.targetHeight + 'px', 'important');
            card.style.setProperty('flex-shrink', '0', 'important');

            const footer = card.nextElementSibling;
            if (footer && footer.className.includes('footer')) {
                footer.style.setProperty('position', 'absolute', 'important');
                footer.style.setProperty('bottom', '0', 'important');
                footer.style.setProperty('left', '0', 'important');
                footer.style.setProperty('right', '0', 'important');
                footer.style.setProperty('max-height', (CONFIG.targetHeight * 0.4) + 'px', 'important');
                footer.style.setProperty('height', 'auto', 'important');
                footer.style.setProperty('padding', '8px', 'important');
                footer.style.setProperty('box-sizing', 'border-box', 'important');
            }
        });

        console.log('[XHS Align] Applied to', cards.length, 'cards');
    };

    window.alignPostHeights = alignPostHeights;

    const init = () => {
        addGlobalStyle();
        setTimeout(alignPostHeights, 2000);

        let timer = null;
        new MutationObserver(() => {
            clearTimeout(timer);
            timer = setTimeout(alignPostHeights, 800);
        }).observe(document.body, { childList: true, subtree: true });
    };

    document.addEventListener('DOMContentLoaded', init);
    if (document.readyState !== 'loading') init();
})();
