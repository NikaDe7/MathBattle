let socket = null;
let timerInterval = null;

// ✅ GOOGLE LOGIN
function handleCredentialResponse(response) {
    if (!response || !response.credential) {
        enterAsGuest();
        return;
    }

    fetch("/auth/google", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: response.credential })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "ok" && data.email) {
            saveUserAndGo({
                name: data.name,
                email: data.email
            });
        } else {
            enterAsGuest();
        }
    })
    .catch(() => enterAsGuest());
}

// ✅ SAVE USER
function saveUserAndGo(user) {
    localStorage.setItem("user", JSON.stringify(user));
    document.getElementById("auth-status").innerText = "Ви увійшли як: " + user.email;
    document.getElementById("to-lobby-btn").style.display = "block";
    showScreen("screen-lobby");
}

// ✅ GUEST
function enterAsGuest() {
    const user = {
        name: "Гість",
        email: "guest_" + Math.random().toString(36).substring(2, 8)
    };
    saveUserAndGo(user);
}

// ✅ START GAME
function handleStartClick() {
    const level = document.getElementById("level-select").value;
    const duration = document.getElementById("duration-select").value;

    showScreen("screen-battle");
    startBattle(level, duration);
}

// ✅ WEBSOCKET & BATTLE
function startBattle(level, duration) {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const userId = user.email || "guest";

    const protocol = location.protocol === "https:" ? "wss:" : "ws:";
    const url = `${protocol}//${location.host}/ws/battle/${encodeURIComponent(userId)}/${level}/${duration}`;

    if (socket) socket.close();
    socket = new WebSocket(url);

    socket.onopen = () => {
        // Запускаємо таймер тільки після успішного відкриття сокета
        startTimer(parseInt(duration));
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.problem) {
            document.getElementById("problem").innerText = data.problem;
        }

        if (data.score !== undefined) {
            document.getElementById("score").innerText = data.score;
        }

        if (data.status === "correct") {
            document.getElementById("answer-input").value = "";
        }
    };

    socket.onclose = () => {
        stopGame();
    };
}

// ✅ TIMER
function startTimer(seconds) {
    clearInterval(timerInterval);
    let time = seconds;

    // Оновлюємо відображення одразу
    updateTimerDisplay(time);

    timerInterval = setInterval(() => {
        time--;
        updateTimerDisplay(time);

        if (time <= 0) {
            stopGame();
            alert("Час вийшов!");
            showScreen("screen-lobby");
        }
    }, 1000);
}

function updateTimerDisplay(time) {
    let m = Math.floor(time / 60);
    let s = time % 60;
    document.getElementById("timer").innerText = `${m}:${s < 10 ? "0" : ""}${s}`;
}

// ✅ STOP
function stopGame() {
    clearInterval(timerInterval);
    if (socket) {
        socket.close();
        socket = null;
    }
}

// ✅ EXIT
function handleExitClick() {
    stopGame();
    showScreen("screen-lobby");
}

// ✅ SCREENS
function showScreen(id) {
    document.querySelectorAll("section").forEach(s => s.style.display = "none");
    const activeSection = document.getElementById(id);
    if (activeSection) {
        activeSection.style.display = "flex";
    }

    if (id === "screen-lobby") {
        loadLeaderboard();
    }

    // Автофокус на поле вводу для швидкої гри
    if (id === "screen-battle") {
        setTimeout(() => {
            const input = document.getElementById("answer-input");
            input.value = "";
            input.focus();
        }, 100);
    }
}

// ✅ LEADERBOARD
function loadLeaderboard() {
    fetch("/leaderboard")
        .then(res => res.json())
        .then(data => updateLeaderboard(data))
        .catch(err => console.error("Помилка завантаження топу:", err));
}

function updateLeaderboard(data) {
    const list = document.getElementById("leaderboard-list");
    list.innerHTML = "";

    if (!data || data.length === 0) {
        list.innerHTML = "<tr><td colspan='4'>Немає даних</td></tr>";
        return;
    }

    data.slice(0, 10).forEach(p => {
        const row = `
            <tr>
                <td>${p.name || "Гість"}</td>
                <td>${p.level || "-"} </td>
                <td>${p.time || "-"}</td>
                <td>${p.score || 0}</td>
            </tr>
        `;
        list.innerHTML += row;
    });
}

// ✅ INITIALIZE & ENTER KEY
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("answer-input");

    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            const val = input.value.trim();
            if (val !== "" && socket && socket.readyState === WebSocket.OPEN) {
                socket.send(val);
            }
        }
    });

    // ВАРІАНТ А: Якщо хочете завжди бачити першу сторінку:
    showScreen("screen-welcome");

    // ВАРІАНТ Б: Якщо хочете залишити автологін, але він глючить,
    // додайте очистку примусово (для тесту):
    // localStorage.clear();
    // showScreen("screen-welcome");
});