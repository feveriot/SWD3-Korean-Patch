-- 헌원검3 한국어 패치 편의 모드 (KoQoL)
-- 원본 스크립트를 바꾸지 않고 원본 함수를 감싸서 동작한다. (모드는 MODsystemMOD 1 이어야 로드됨)
-- 단축키: F4 설정표 켜기/끄기, F5 필드 전투(보통→2→4배→0), F6 이동 속도(1→1.5→2배), F7 돈(1→2→4배), F8 경험치(1→2→4배)
-- (자동 전투·전투 속도는 효과가 없어 제외)
KoQoL = KoQoL or {}
KoQoL.wrapped = KoQoL.wrapped or {}
OnEvent = OnEvent or {}

local function wrap(name, maker)
    local t = OnEvent[name]
    if type(t) ~= 'table' or type(t.main) ~= 'function' then return end
    if t.main == KoQoL.wrapped[name] then return end
    local w = maker(t.main)
    t.main = w
    KoQoL.wrapped[name] = w
end

-- 설정값 (세이브에 저장)
function KoQoL.Cfg()
    if not SaveData then return {Enc = 1, Money = 1, Exp = 1, Move = 1} end
    SaveData.KoQoL = SaveData.KoQoL or {}
    local c = SaveData.KoQoL
    if c.AutoOff == nil then c.AutoOff = false end
    if c.Enc == nil then c.Enc = (c.EncOff and 0) or 1 end -- 이전 버전 켬/끔 값 이어받기
    if c.Enc ~= 0 and c.Enc ~= 2 and c.Enc ~= 4 then c.Enc = 1 end
    local function norm(v) if v == 2 or v == 4 then return v end return 1 end
    c.Money = norm(c.Money); c.Exp = norm(c.Exp)
    if c.Move ~= 1.5 and c.Move ~= 2 then c.Move = 1 end
    return c
end

local KEYS = {[61] = 'show', [62] = 'enc', [63] = 'move', [64] = 'money', [65] = 'exp'} -- F4 표시, F5~F8
local function nextm(v) if v == 1 then return 2 elseif v == 2 then return 4 end return 1 end

function KoQoL.Toggle(what)
    if not what or not SaveData then return end
    if GameFunc and GameFunc.InBattle then return end
    local now = GetTicks and GetTicks() or 0
    if KoQoL.last and now - KoQoL.last < 200 then return end
    KoQoL.last = now
    KoQoL.showUntil = now + 3000 -- 키를 누르면 3초간 표시
    if what == 'show' then KoQoL.pin = not KoQoL.pin return end
    local c = KoQoL.Cfg(); local on
    if what == 'enc' then
        if c.Enc == 1 then c.Enc = 2 elseif c.Enc == 2 then c.Enc = 4 elseif c.Enc == 4 then c.Enc = 0 else c.Enc = 1 end
        on = c.Enc > 0
    elseif what == 'move' then
        if c.Move == 1 then c.Move = 1.5 elseif c.Move == 1.5 then c.Move = 2 else c.Move = 1 end
        on = c.Move > 1; KoQoL.ApplyMove()
    elseif what == 'money' then c.Money = nextm(c.Money); on = c.Money > 1
    elseif what == 'exp' then c.Exp = nextm(c.Exp); on = c.Exp > 1
    end
    if MediaFunc then if on then MediaFunc.PlaySound(46) else MediaFunc.PlaySound(45) end end
end
function KoQoL.Key(Key_SCANCODE) KoQoL.Toggle(KEYS[Key_SCANCODE]) end

-- 이동 속도: 맵 데이터의 BasicSpeed(마을 4, 월드맵 2)를 배율로 조정. 다음 맵 이동부터 적용
KoQoL.baseSpeed = KoQoL.baseSpeed or {}
function KoQoL.ApplyMove()
    if not (GameData and type(GameData.MapDetail) == 'table') then return end
    local m = KoQoL.Cfg().Move or 1
    for id, d in pairs(GameData.MapDetail) do
        if type(d) == 'table' and type(d.BasicSpeed) == 'number' then
            if KoQoL.baseSpeed[id] == nil then KoQoL.baseSpeed[id] = d.BasicSpeed end
            d.BasicSpeed = math.max(1, math.floor(KoQoL.baseSpeed[id] * m + 0.5))
        end
    end
end
function KoQoL.SpdRestore() end

-- 설정 메뉴 빈칸 위치 (논리 좌표)
local DX, DY, DH = 230, 236, 25
-- 표시 문자열: lua 안 한글은 깨지므로 en\StringDB.txt(9901~)에서 가져오고, 없으면 영어
local function S(k, fb)
    for _, key in ipairs({'KoQoL_' .. k}) do
        local ok, v = pcall(StringDB, key)
        if ok and type(v) == 'string' and v ~= '' and v ~= key then return v end
    end
    return fb
end

function KoQoL.Draw()
    KoQoL.SpdRestore()
    -- 타이틀 화면에는 표시하지 않음: 주인공 파티 플래그(30)가 켜진 게임 중에만
    local ok, inparty = pcall(function() return GameFunc.GetFlag(30) end)
    if not (ok and inparty) then return end
    -- 메뉴 종류를 알 수 없어 항상 띄우지 않음: F4로 고정 표시, 또는 F4~F9 누른 뒤 3초간
    local now = GetTicks and GetTicks() or 0
    if not KoQoL.pin and not (KoQoL.showUntil and now < KoQoL.showUntil) then return end
    if not StringFunc or not DrawFunc then return end
    local c = KoQoL.Cfg()
    local f = DrawFunc.Color(247, 232, 186, 255)
    local h = DrawFunc.Color(255, 220, 120, 255)
    local b = DrawFunc.Color(30, 20, 10, 200)
    local on, off, x = S('On', 'ON'), S('Off', 'OFF'), S('X', 'x')
    local function mult(v) if v == 1 then return S('Normal', 'Normal') end return tostring(v) .. x end
    local rows = {
        {S('Field', 'Field battle') .. ' (F5)', (c.Enc == 0 and off) or mult(c.Enc)},
        {S('Move', 'Move speed') .. ' (F6)', (c.Move == 1 and S('Normal', 'Normal')) or (tostring(c.Move) .. x)},
        {S('Money', 'Battle money') .. ' (F7)', mult(c.Money)},
        {S('Exp', 'Battle EXP') .. ' (F8)', mult(c.Exp)},
    }
    for i, r in ipairs(rows) do
        local y = DY + (i - 1) * DH
        StringFunc.DrawString(r[1], DX, y, 1, f, b, 1)
        StringFunc.DrawString(r[2], DX + 170, y, 1, h, b, 1)
    end
end

function KoQoL.Patch()
    wrap('MapLoading', function(orig) return function(...)
        KoQoL.ApplyMove()
        return orig(...)
    end end)
    for _, nm in ipairs({'MapLoaded', 'GameStart'}) do
        wrap(nm, function(orig) return function(...)
            KoQoL.inGame = true
            return orig(...)
        end end)
    end
    wrap('PlayerMove', function(orig) return function(...)
        KoQoL.SpdRestore()
        local e = KoQoL.Cfg().Enc
        if e == 0 then GameFunc.PlayerBattleStepCount = 0 return end
        -- 2배·4배: 걸음 수를 더 세어 전투 발생 간격을 1/2·1/4로
        if e > 1 and not GameFunc.InBattle and type(GameFunc.PlayerBattleStepCount) == 'number' then
            GameFunc.PlayerBattleStepCount = GameFunc.PlayerBattleStepCount + (e - 1)
        end
        return orig(...)
    end end)

    wrap('Battle_PlayerInit', function(orig) return function(index, ...)
        local r = orig(index, ...)
        local p = BattlePlayers and BattlePlayers[index]
        return r
    end end)

    wrap('BattleGain', function(orig) return function(...)
        local r = orig(...)
        local c = KoQoL.Cfg()
        if OnEventValue and type(OnEventValue.Money) == 'number' and c.Money > 1 then OnEventValue.Money = OnEventValue.Money * c.Money end
        if OnEventValue and type(OnEventValue.PlayerExp) == 'number' and c.Exp > 1 then OnEventValue.PlayerExp = OnEventValue.PlayerExp * c.Exp end
        return r
    end end)

    wrap('InputKeyDown', function(orig) return function(KeyFunc_flag, Key_SCANCODE, ...)
        KoQoL.Key(Key_SCANCODE)
        return orig(KeyFunc_flag, Key_SCANCODE, ...)
    end end)

    wrap('DrawMenuAfter', function(orig) return function(...)
        local r = orig(...)
        KoQoL.Draw()
        return r
    end end)
end

for _, ev in ipairs({'SysInit', 'GameStart', 'MapLoaded', 'MapLoading', 'Battle_Enter'}) do
    OnEvent[ev] = OnEvent[ev] or {}
    OnEvent[ev][95] = KoQoL.Patch
end
KoQoL.Patch()
