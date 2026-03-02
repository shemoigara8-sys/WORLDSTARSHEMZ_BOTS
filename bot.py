const TelegramBot = require('node-telegram-bot-api');

const token = "8704352560:AAEVi4SbL9brYht1zLAp0BTnNjaLdVL6b60";
const adminId = "6764405064";

const bot = new TelegramBot(token, { polling: true });

let users = {};

function basePrice(type) {
    switch (type.toLowerCase()) {
        case "restaurant": return 15000;
        case "portfolio": return 10000;
        case "blog": return 8000;
        case "school": return 20000;
        case "company website": return 25000;
        case "e-commerce": return 35000;
        default: return 12000;
    }
}

bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;

    users[chatId] = { step: 1 };

    bot.sendMessage(
        chatId,
        "👋 Welcome to WorldStarShemz Web Services!\n\nWhat type of website do you want?",
        {
            reply_markup: {
                keyboard: [
                    ["Restaurant", "E-commerce"],
                    ["Portfolio", "School"],
                    ["Blog", "Company Website"]
                ],
                resize_keyboard: true,
                one_time_keyboard: true
            }
        }
    );
});

bot.on("message", (msg) => {
    const chatId = msg.chat.id;

    if (!users[chatId] || msg.text === "/start") return;

    const user = users[chatId];

    switch (user.step) {

        case 1:
            user.websiteType = msg.text;
            user.totalPrice = basePrice(msg.text);
            user.breakdown = "Base price: KES " + user.totalPrice + "\n";
            user.step++;
            bot.sendMessage(chatId, "🏢 What is your business name?");
            break;

        case 2:
            user.businessName = msg.text;
            user.step++;
            bot.sendMessage(chatId, "📄 How many pages do you need? (Enter number only)");
            break;

        case 3:
            user.pages = parseInt(msg.text);

            if (isNaN(user.pages)) {
                bot.sendMessage(chatId, "Please enter a valid number of pages.");
                return;
            }

            if (user.pages > 5) {
                let extra = (user.pages - 5) * 2000;
                user.totalPrice += extra;
                user.breakdown += "Extra pages cost: KES " + extra + "\n";
            }

            user.step++;
            bot.sendMessage(
                chatId,
                "⚙️ Type the features you need (example: payment, booking, chatbot).\nIf none, type: none"
            );
            break;

        case 4:
            let featuresText = msg.text.toLowerCase();

            if (featuresText.includes("payment")) {
                user.totalPrice += 7000;
                user.breakdown += "Online payment: KES 7000\n";
            }

            if (featuresText.includes("booking")) {
                user.totalPrice += 5000;
                user.breakdown += "Booking system: KES 5000\n";
            }

            if (featuresText.includes("chatbot")) {
                user.totalPrice += 4000;
                user.breakdown += "Chatbot: KES 4000\n";
            }

            user.features = msg.text;
            user.step++;
            bot.sendMessage(chatId, "⏳ In how many days do you need the website ready? (Enter number)");
            break;

        case 5:
            let days = parseInt(msg.text);

            if (isNaN(days)) {
                bot.sendMessage(chatId, "Please enter a valid number of days.");
                return;
            }

            if (days < 7) {
                user.totalPrice += 5000;
                user.breakdown += "Rush fee: KES 5000\n";
            }

            user.deadline = days + " days";
            user.step++;
            bot.sendMessage(chatId, "📞 Please provide your phone number or email.");
            break;

        case 6:
            user.contact = msg.text;
            user.step++;
            bot.sendMessage(
                chatId,
                "🎨 Do you have existing brand colors or design preferences?",
                {
                    reply_markup: {
                        keyboard: [
                            ["Yes, I have a design", "No, surprise me"],
                            ["Modern & Minimal", "Colorful & Creative"]
                        ],
                        resize_keyboard: true,
                        one_time_keyboard: true
                    }
                }
            );
            break;

        case 7:
            user.designPreference = msg.text;
            user.step++;
            bot.sendMessage(
                chatId,
                "📱 Do you need the website to be mobile-friendly?",
                {
                    reply_markup: {
                        keyboard: [
                            ["Yes, fully responsive", "Basic mobile support", "Not required"]
                        ],
                        resize_keyboard: true,
                        one_time_keyboard: true
                    }
                }
            );
            break;

        case 8:
            user.mobileSupport = msg.text;
            if (user.mobileSupport.toLowerCase().includes("fully responsive")) {
                user.totalPrice += 3000;
                user.breakdown += "Fully responsive design: KES 3000\n";
            }
            user.step++;
            bot.sendMessage(
                chatId,
                "🔍 Do you need SEO optimization?",
                {
                    reply_markup: {
                        keyboard: [
                            ["Yes", "No"]
                        ],
                        resize_keyboard: true,
                        one_time_keyboard: true
                    }
                }
            );
            break;

        case 9:
            user.seo = msg.text;
            if (user.seo.toLowerCase() === "yes") {
                user.totalPrice += 4000;
                user.breakdown += "SEO Optimization: KES 4000\n";
            }
            user.step++;
            bot.sendMessage(
                chatId,
                "🖼️ Do you have existing content (text, images, videos)?",
                {
                    reply_markup: {
                        keyboard: [
                            ["Yes, I have content", "No, need help creating"],
                            ["Partially ready"]
                        ],
                        resize_keyboard: true,
                        one_time_keyboard: true
                    }
                }
            );
            break;

        case 10:
            user.contentStatus = msg.text;
            if (user.contentStatus.toLowerCase().includes("help")) {
                user.totalPrice += 5000;
                user.breakdown += "Content creation: KES 5000\n";
            }
            user.step++;
            bot.sendMessage(
                chatId,
                "🛡️ Do you need SSL certificate and domain registration?",
                {
                    reply_markup: {
                        keyboard: [
                            ["Yes, both", "Only SSL", "Only domain", "I have both"]
                        ],
                        resize_keyboard: true,
                        one_time_keyboard: true
                    }
                }
            );
            break;

        case 11:
            user.sslDomain = msg.text;
            if (user.sslDomain.toLowerCase().includes("yes") || user.sslDomain.toLowerCase().includes("ssl")) {
                user.totalPrice += 3000;
                user.breakdown += "SSL & Domain setup: KES 3000\n";
            }
            user.step++;
            bot.sendMessage(
                chatId,
                "📊 Do you need analytics and reporting?",
                {
                    reply_markup: {
                        keyboard: [
                            ["Yes", "No"]
                        ],
                        resize_keyboard: true,
                        one_time_keyboard: true
                    }
                }
            );
            break;

        case 12:
            user.analytics = msg.text;
            if (user.analytics.toLowerCase() === "yes") {
                user.totalPrice += 2000;
                user.breakdown += "Analytics & Reporting: KES 2000\n";
            }
            user.step++;
            bot.sendMessage(
                chatId,
                "🔧 Will you need ongoing maintenance and support after launch?",
                {
                    reply_markup: {
                        keyboard: [
                            ["Yes, monthly support", "One-time only", "Not sure yet"]
                        ],
                        resize_keyboard: true,
                        one_time_keyboard: true
                    }
                }
            );
            break;

        case 13:
            user.maintenance = msg.text;
            user.step++;
            bot.sendMessage(
                chatId,
                "💼 Who should we contact for approval and updates?",
                {
                    reply_markup: {
                        keyboard: [
                            ["Me (owner)", "Project manager", "Multiple contacts"]
                        ],
                        resize_keyboard: true,
                        one_time_keyboard: true
                    }
                }
            );
            break;

        case 14:
            user.contactPerson = msg.text;
            user.step++;
            bot.sendMessage(chatId, "📝 Any additional notes or special requirements? (Type 'none' if not applicable)");
            break;

        case 15:
            user.additionalNotes = msg.text;

            // Send detailed order to admin
            bot.sendMessage(
                adminId,
                "🔥 NEW SMART WEBSITE ORDER 🔥\n\n" +
                "👤 CLIENT DETAILS:\n" +
                "Business: " + user.businessName + "\n" +
                "Contact: " + user.contact + "\n" +
                "Contact Person: " + user.contactPerson + "\n\n" +
                "🌐 PROJECT DETAILS:\n" +
                "Type: " + user.websiteType + "\n" +
                "Pages: " + user.pages + "\n" +
                "Features: " + user.features + "\n" +
                "Deadline: " + user.deadline + "\n\n" +
                "🎨 DESIGN & TECH:\n" +
                "Design Preference: " + user.designPreference + "\n" +
                "Mobile Support: " + user.mobileSupport + "\n" +
                "SEO: " + user.seo + "\n" +
                "Content Status: " + user.contentStatus + "\n" +
                "SSL/Domain: " + user.sslDomain + "\n" +
                "Analytics: " + user.analytics + "\n\n" +
                "🛠️ SUPPORT:\n" +
                "Maintenance: " + user.maintenance + "\n" +
                "Notes: " + user.additionalNotes + "\n\n" +
                "💰 PRICING:\n" +
                user.breakdown +
                "------------------------\n" +
                "💰 TOTAL: KES " + user.totalPrice
            );

            // Send breakdown to client
            bot.sendMessage(
                chatId,
                "📊 PRICE BREAKDOWN\n\n" +
                user.breakdown +
                "------------------------\n" +
                "💰 TOTAL: KES " + user.totalPrice + "\n\n" +
                "Payment will be made AFTER completion.\n\n" +
                "📲 Send payment to: 0719369552\n\n" +
                "We will contact you shortly 🚀"
            );

            delete users[chatId];
            break;
    }
});
