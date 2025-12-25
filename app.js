import { GoogleGenerativeAI } from "https://esm.run/@google/generative-ai";

const interpretBtn = document.getElementById('interpretBtn');
const dreamInput = document.getElementById('dreamInput');
// const apiKeyInput = document.getElementById('apiKey'); // Removed
const resultCard = document.getElementById('resultCard');
const resultContent = document.getElementById('resultContent');
const loadingState = document.getElementById('loadingState');
const emptyState = document.getElementById('emptyState');
const toastContainer = document.getElementById('toastContainer');

// Localization
const langToggle = document.getElementById('langToggle');
let currentLang = 'en';

const translations = {
    en: {
        badgeText: "AI Powered",
        appTitle: "Dream Interpreter",
        appDescription: "Unlock the hidden meanings behind your dreams using the power of Gemini AI.",
        langToggle: "العربية",
        inputTitle: "Your Dream",
        inputLabel: "Describe your dream",
        dreamInputPlaceholder: "I was flying over a city made of crystal...",
        interpretBtn: "Interpret Dream",
        resultTitle: "Interpretation",
        loadingText: "Consulting the oracle...",
        emptyText: "Enter your dream to reveal its meaning.",
        toastSuccess: "Dream interpreted successfully",
        toastError: "Failed to interpret dream. Check your API key.",
        toastEmpty: "Please describe your dream"
    },
    ar: {
        badgeText: "مدعوم بالذكاء الاصطناعي",
        appTitle: "مفسر الأحلام",
        appDescription: "اكتشف المعاني الخفية وراء أحلامك باستخدام قوة Gemini AI.",
        langToggle: "English",
        inputTitle: "حلمك",
        inputLabel: "صف حلمك",
        dreamInputPlaceholder: "كنت أطير فوق مدينة مصنوعة من الكريستال...",
        interpretBtn: "فسر الحلم",
        resultTitle: "التفسير",
        loadingText: "جاري استشارة العراف...",
        emptyText: "أدخل حلمك للكشف عن معناه.",
        toastSuccess: "تم تفسير الحلم بنجاح",
        toastError: "فشل تفسير الحلم. تحقق من مفتاح API.",
        toastEmpty: "الرجاء وصف حلمك"
    }
};

function setLanguage(lang) {
    currentLang = lang;
    const t = translations[lang];
    const dir = lang === 'ar' ? 'rtl' : 'ltr';

    document.documentElement.dir = dir;
    document.documentElement.lang = lang;

    // Update Text
    document.getElementById('badgeText').textContent = t.badgeText;
    document.getElementById('appTitle').textContent = t.appTitle;
    document.getElementById('appDescription').textContent = t.appDescription;
    document.getElementById('langToggle').textContent = t.langToggle;
    document.getElementById('inputTitle').textContent = t.inputTitle;
    document.getElementById('inputLabel').textContent = t.inputLabel;
    document.getElementById('dreamInput').placeholder = t.dreamInputPlaceholder;
    document.getElementById('interpretBtn').textContent = t.interpretBtn;
    document.getElementById('resultTitle').textContent = t.resultTitle;
    document.getElementById('loadingText').textContent = t.loadingText;
    document.getElementById('emptyText').textContent = t.emptyText;
}

langToggle.addEventListener('click', () => {
    const newLang = currentLang === 'en' ? 'ar' : 'en';
    setLanguage(newLang);
});

// Helper to show toast
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast';

    const icon = type === 'success' ? '✓' : '!';
    const colorClass = type === 'success' ? 'success' : 'error'; // We'll just use inline styles for simplicity or the alert classes if we had them in toast

    // Using the design system's toast structure
    toast.innerHTML = `
        <div class="icon-box" style="width: 24px; height: 24px; margin-bottom: 0; border: none;">${icon}</div>
        <div>
            <div style="font-weight: bold;">${type === 'success' ? 'Success' : 'Error'}</div>
            <div style="font-size: 0.875rem; opacity: 0.8;">${message}</div>
        </div>
    `;

    toastContainer.appendChild(toast);

    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

interpretBtn.addEventListener('click', async () => {
    const dream = dreamInput.value.trim();
    // Hardcoded API Key as requested
    const apiKey = "AIzaSyBMmw_RjaaB-M1FrXy6RKtymkg0Q5AuMQc";

    if (!dream) {
        showToast(translations[currentLang].toastEmpty, 'error');
        return;
    }

    // UI State: Loading
    interpretBtn.disabled = true;
    emptyState.style.display = 'none';
    resultCard.style.display = 'none';
    loadingState.style.display = 'block';

    try {
        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({ model: "gemini-flash-latest" });

        let prompt = `You are a mystical and insightful dream interpreter. Interpret the following dream: "${dream}". Provide a concise but deep analysis of the symbolism and potential meaning. Keep the tone mysterious but helpful.`;

        if (currentLang === 'ar') {
            prompt = `أنت مفسر أحلام خبير في التراث الإسلامي وتفسير الأحلام لابن سيرين والنابلسي.
            قم بتفسير الحلم التالي: "${dream}".
            
            قواعد التفسير:
            1. ابحث عن الرموز في الحلم وفسرها بناءً على كتب ابن سيرين والنابلسي.
            2. قدم التفسير بشكل موجز ومفيد.
            3. استشهد بدلالات الرموز كما وردت في التراث الإسلامي إن أمكن.
            4. حافظ على نبرة مطمئنة وحكيمة.
            5. ابدأ بعبارة "والله أعلم" في النهاية.
            
            رد باللغة العربية.`;
        }

        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text();

        // UI State: Success
        loadingState.style.display = 'none';
        resultCard.style.display = 'block';

        // Simple markdown parsing (bolding)
        const formattedText = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');

        resultContent.innerHTML = formattedText;
        showToast(translations[currentLang].toastSuccess);

    } catch (error) {
        console.error(error);
        loadingState.style.display = 'none';
        emptyState.style.display = 'block';
        showToast(translations[currentLang].toastError, 'error');
    } finally {
        interpretBtn.disabled = false;
    }
});
