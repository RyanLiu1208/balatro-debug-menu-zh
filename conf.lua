-- 按住 Tab 显示内置调试菜单，松开关闭。
-- Hold Tab to show the built-in debug menu; release it to close.
-- 中文菜单文案需要另行应用界面补丁，见 README。
-- Chinese menu labels require the UI patch described in README.

_RELEASE_MODE = false -- 开启内置调试功能 / Enable built-in debug tools
_DEMO = false         -- 保持完整游戏模式 / Keep the full game mode

function love.conf(t)
    t.console = false -- 不显示黑色控制台 / Hide the black console window
    t.title = 'Balatro'
    t.window.width = 0
    t.window.height = 0
    t.window.minwidth = 100
    t.window.minheight = 100
end
