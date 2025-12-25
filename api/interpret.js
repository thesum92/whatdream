import { GoogleGenerativeAI } from "@google/generative-ai";

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
        return res.status(500).json({ error: 'Server configuration error: Missing API Key' });
    }

    const { dream, language } = req.body;

    if (!dream) {
        return res.status(400).json({ error: 'Dream text is required' });
    }

    try {
        const genAI = new GoogleGenerativeAI(apiKey);
        // Using the model we verified works
        const model = genAI.getGenerativeModel({ model: "gemini-flash-latest" });

        let prompt = `You are an expert dream interpreter specializing in Islamic tradition, specifically the works of Ibn Sirin and Al-Nabulsi.
        Interpret the following dream: "${dream}".
        
        Interpretation Rules:
        1. Identify symbols in the dream and interpret them based on the books of Ibn Sirin and Al-Nabulsi.
        2. Provide a concise and helpful interpretation.
        3. Cite the meanings of symbols as found in Islamic tradition where possible.
        4. Maintain a reassuring and wise tone.
        5. End with the phrase "And Allah knows best."
        
        Respond in English.`;

        if (language === 'ar') {
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

        return res.status(200).json({ result: text });

    } catch (error) {
        console.error("Gemini API Error:", error);
        return res.status(500).json({ error: 'Failed to interpret dream' });
    }
}
