import { marked } from "https://esm.run/marked";

// Localization
const langToggle = document.getElementById('langToggle');
let currentLang = 'ar';

const interpretBtn = document.getElementById('interpretBtn');
const dreamInput = document.getElementById('dreamInput');
const resultCard = document.getElementById('resultCard');
const resultContent = document.getElementById('resultContent');
const loadingState = document.getElementById('loadingState');
const emptyState = document.getElementById('emptyState');
const toastContainer = document.getElementById('toastContainer');


const translations = {
    en: {
        badgeText: "Instant AI Interpretation",
        appTitle: "Dream Interpretation - Ibn Sirin & Nabulsi",
        appDescription: "Interpret your dream now for free and accurately. We combine the authenticity of Ibn Sirin & Nabulsi with Advanced AI to reveal your vision's secrets.",
        langToggle: "العربية",
        inputTitle: "Your Dream",
        inputLabel: "Describe your dream",
        dreamInputPlaceholder: "I was flying over a city made of crystal...",
        interpretBtn: "Interpret Dream",
        resultTitle: "Interpretation",
        loadingText: "Consulting the oracle...",
        emptyText: "Enter your dream to reveal its meaning.",
        toastSuccess: "Dream interpreted successfully",
        toastError: "Failed to interpret dream.",
        toastEmpty: "Please describe your dream"
    },
    ar: {
        badgeText: "تفسير فوري بالذكاء الاصطناعي",
        appTitle: "تفسير الأحلام - ابن سيرين والنابلسي",
        appDescription: "فسّر حلمك الآن مجاناً وبدقة. نجمع بين أصالة تفسير ابن سيرين والنابلسي وتقنيات الذكاء الاصطناعي لكشف خفايا رؤياك.",
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
        const response = await fetch('/api/interpret', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                dream: dream,
                language: currentLang
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to interpret');
        }

        const text = data.result;

        // UI State: Success
        loadingState.style.display = 'none';
        resultCard.style.display = 'block';

        // Markdown parsing with marked
        const formattedText = marked.parse(text);

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
