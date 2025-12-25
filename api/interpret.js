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

        const englishMethodology = `
# The Interpretative Architect: Reverse-Engineering Ibn Sirin’s Methodology

## Phase 1: Deep Analytical Audit

Upon analyzing the dataset of Ibn Sirin’s interpretations, it becomes evident that his approach is not a mere dictionary of symbols, but a rigorous semiotic system rooted in **linguistic determinism**, **theological precedent**, and **functional analogy**.

### Core Interpretative Modes

1.  **Linguistic & Etymological Isomorphism (The Root System)**
    *   **Logic:** The meaning of a symbol is often locked within the trilateral root of its Arabic name. The signifier (the word) *dictates* the signified (the meaning).
    *   **Evidence:**
        *   **Needle (Ibrah):** Derived from specific roots implying "joining". In the text: *"The advisor (Naseeh) is from the language of the Arabs meaning the tailor."* Thus, a needle represents an advisor or a wife because it "joins" things together.
        *   **Furniture/Earth:** The text often links names to functional outcomes based on phonetic similarity or shared roots.

2.  **Scriptural Archetypes (Quranic Intertextuality)**
    *   **Logic:** If a symbol appears in the Quran, its Quranic context overrides its physical reality.
    *   **Evidence:**
        *   **Rope (Habl):** Interpreted as a "Covenant" or "Pact" based on the verse *"And hold is firmly to the rope of Allah..."*
        *   **Iblis/Satan:** Represents "Deception" or "Envy" specifically citing the story of Adam.
        *   **"Uff" (Expression of annoyance):** Interpreted as "Disobedience to parents" citing *"Do not say to them 'Uff'..."*

3.  **Functional & Physical Analogy (Al-Qiyas)**
    *   **Logic:** An object's function in waking life translates directly to its function in the dream world, often abstracting the *action* rather than the *object*.
    *   **Evidence:**
        *   **Kiln/Furnace:** A place where material acts are transformed by heat. In the text, it represents the "Treasury" or "Authority" because it collects and processes resources.
        *   **Ear:** The organ of hearing becomes the "Spy" (who hears) or the "King’s Messenger".

4.  **Contextual Relativism (The "State" Filter)**
    *   **Logic:** A symbol has no fixed meaning; its polarity (positive/negative) is determined by the dreamer's waking status (Health, Wealth, Profession).
    *   **Evidence:**
        *   **The Sick:** Almost every symbol has a specific, often morbid variation for the sick (e.g., Entering a house -> Tomb; Perfume -> Funeral rites).
        *   **The Single vs. Married:** A symbol like "Ar-Rida" (Cloak) means "Marriage" for the single (it covers/protects them) but might mean "Protection/Status" for the married.

---

## Phase 2: The Interpretative Methodology Guide

To interpret like Ibn Sirin, one must follow this recursive logic flow:

### Step 1: The Linguistic Audit
**Question:** What is the Arabic name of the object? Does its root imply a specific action (e.g., Opening, Binding, Rising, Cutting)?
*   *Rule:* If the name sounds like "Victory" (Nasr), the symbol is Victory, regardless of what the object actually is.

### Step 2: The Scriptural Scan
**Question:** Is this object mentioned in a Holy Text (Quran/Hadith)?
*   *Rule:* If yes, apply the *context of the verse*.
    *   *Example:* A "Ship" is always "Safety/Salvation" (referencing Noah).

### Step 3: Functional Abstraction
**Question:** What does this object *do*?
*   *Rule:* Convert the object into a verb.
    *   *Pen* -> Records/Decides -> Interpretation: A Judge or Ruler.
    *   *Key* -> Opens/Locks -> Interpretation: Access to wealth or answering of prayers.

### Step 4: The Contextual Filter (The Principles of Contextualization)
Apply the specific variables of the dreamer to the core meaning derived above:

| Variable | Logic Modifier | Example (Symbol: Fire) |
| :--- | :--- | :--- |
| **Profession** | Does the symbol aid or hinder their work? | **Blacksmith:** Profit/Success. <br> **Farmer:** Destruction/Drought. |
| **Health** | Is the dreamer physically vulnerable? | **Healthy:** Power/Energy. <br> **Sick:** Fever/Death. |
| **Season** | Is the symbol appropriate for the time? | **Rain (Winter):** Mercy/Fertility. <br> **Rain (Summer):** Disease/Disruption. |
| **Status** | Is the dreamer Single or Married? | **Garment:** Marriage (for single). <br> **Garment:** Status/Wealth (for married). |

---

## Phase 3: Modern Application & Synthesis

Applying Ibn Sirin’s semiotic engine to the 21st century.

### 1. The Smartphone
*   **Linguistic/Functional:** It transmits voices (Hatif) and holds secrets (Asrar). It connects the distant (Silah).
*   **Methodology:**
    *   *Root:* "Hatif" (Voice from the unseen).
    *   *Function:* Connection, Knowledge, Archive.
*   **Interpretation:**
    *   **General:** A "Messenger" or "News Carrier". It represents the dreamer's connection to the world.
    *   **Broken Screen:** A rift in relationships or a "Misunderstanding" (distortion of the message).
    *   **Loss:** Severing ties (Qat' ar-rahm) or exposure of secrets (Fadhiha).
    *   **For the Single:** Breaking news of a proposal.

### 2. The Airplane
*   **Analogy:** The "Ship" of the sky.
*   **Methodology:**
    *   *Scriptural Parrallel:* "And He created for them the likes of it which they ride."
    *   *Function:* High speed elevation, travel, transport.
*   **Interpretation:**
    *   **Ascending:** Rapid rise in social status or spiritual rank (Ref: Ascent/Mi'raj).
    *   **Landing:** Stability after a period of volatility.
    *   **Crash:** A sudden, catastrophic fall from grace or failure of a major ambition.
    *   **For the Sick:** A journey to the afterlife (ascending towards the heavens).

### 3. Cryptocurrency / Digital Wallet
*   **Analogy:** "Batin" (Hidden) Wealth or "Wadi'ah" (Trust/Deposit).
*   **Function:** Invisible value, volatile, encrypted (sealed).
*   **Interpretation:**
    *   **Wallet:** Secret Knowledge or "Hidden Treasures" (Kanz).
    *   **Losing Key:** Betraying a trust or forgetting a crucial testimony.
    *   **Mining:** Exerting effort for "Ilm" (Knowledge) that yields "Mal" (Wealth).

### 4. Complex Narrative Synthesis
**Dream:** *A user dreams they are flying an airplane at night using a smartphone as the controller, but the battery dies.*

*   **Deconstruction:**
    *   **Flying (Night):** Unclear/Ambiguous Journey or Spiritual Ambition veiled in mystery.
    *   **Smartphone Controller:** The dreamer is navigating their life via "News/Information" or "Social Connections."
    *   **Battery Dies:** The "Energy" or "Life Force" runs out. Loss of capacity.
*   **Synthesis:** The dreamer is attempting a high-risk rapid ascent in their career or status relying heavily on *social influence* or *information* (Smartphone) rather than solid foundations. The "battery dying" warns that their *resource/energy* (or the patience of their connection) is about to run out, leading to a loss of control before the destination is reached.

        **Task:**
        Interpret the following dream: "${dream}"

        **Output Requirements:**
        - ACT AS an expert following the methodology above strictly.
        - Start with a direct, wise interpretation using the methodology above.
        - Cite specific linguistic roots or scriptural references where applicable.
        - Be concise but profound.
        - Maintain a reassuring tone.
        - End with: "And Allah knows best."
        `;

        const arabicMethodology = `
# المهندس التأويلي: هندسة عكسية لمنهجية ابن سيرين

## المرحلة الأولى: التدقيق التحليلي العميق

من خلال تحليل بيانات تفسيرات ابن سيرين، يتضح أن منهجه ليس مجرد قاموس للرموز، بل هو نظام سيميائي دقيق يرتكز على **الحتمية اللغوية**، **السابقة الشرعية**، و**القياس الوظيفي**.

### أنماط التأويل الأساسية

1. **التماثل اللغوي والاشتقاقي (نظام الجذور)**
    * **المنطق:** المعنى غالبًا ما يكون كامنًا في الجذر الثلاثي للاسم العربي. الدال (الكلمة) *يملي* المدلول (المعنى).
    * **الدليل:**
        * **الإبرة:** مشتقة من جذور تعني الجمع والالتحام. في النص: *"والنصاح في لغة العرب الخياط"*. وبالتالي، الإبرة تدل على الناصح أو الزوجة لأنها "تجمع" الأشياء المتفرقة.
        * **الأثاث/الأرض:** يربط النص غالبًا الأسماء بالنتائج الوظيفية بناءً على التشابه الصوتي أو الجذور المشتركة.

2. **النماذج الأصلية في النصوص الشرعية (التناص القرآني)**
    * **المنطق:** إذا ورد الرمز في القرآن الكريم، فإن السياق القرآني يغلب واقعه المادي.
    * **الدليل:**
        * **الحبل:** يُفسر على أنه "عهد" أو "ميثاق" استنادًا إلى الآية *"واعتصموا بحبل الله جميعاً..."*.
        * **إبليس:** يدل على "المكر" أو "الحسد" استحضارًا لقصته مع آدم عليه السلام.
        * **أف:** تُفسر على أنها "عقوق الوالدين" استنادًا إلى الآية *"فلا تقل لهما أف..."*.

3. **القياس الوظيفي والمادي**
    * **المنطق:** وظيفة الشيء في اليقظة تترجم مباشرة إلى وظيفته في عالم الأحلام، وغالبًا ما يتم تجريد *الفعل* بدلاً من *الشيء* نفسه.
    * **الدليل:**
        * **الكور/التنور:** مكان تتحول فيه المواد بالحرارة. في النص، يمثل "بيت المال" أو "السلطة" لأنه يجمع الموارد ويعالجها.
        * **الأذن:** عضو السمع يصبح "الجاسوس" (الذي يسمع) أو "رسول الملك".

4. **النسبية السياقية (مرشح "الحال")**
    * **المنطق:** الرمز ليس له معنى ثابت؛ تقاطبه (إيجابي/سلبي) يتحدد بحالة الرائي في اليقظة (الصحة، الغنى، المهنة).
    * **الدليل:**
        * **المريض:** كل رمز تقريبًا له تنويعة خاصة، وغالبًا ما تكون مشؤومة للمريض (مثلاً، دخول الدار -> القبر؛ التطيب -> تجهيز الميت).
        * **الأعزب مقابل المتزوج:** رمز مثل "الرداء" يعني "الزواج" للأعزب (لأنه يستر/يحصن) ولكنه قد يعني "الجاه/الستر" للمتزوج.

---

## المرحلة الثانية: دليل المنهجية التأويلية

لتفسير الأحلام بمنهجية ابن سيرين، يجب اتباع هذا التسلسل المنطقي التكراري:

### الخطوة 1: التدقيق اللغوي
**السؤال:** ما هو الاسم العربي للشيء؟ هل يشير جذره إلى فعل معين (مثل: الفتح، الربط، الصعود، القطع)؟
* *القاعدة:* إذا كان الاسم يشبه "نصر"، فالرمز هو النصر، بغض النظر عما هو الشيء في الواقع.

### الخطوة 2: المسح الشرعي
**السؤال:** هل ورد هذا الشيء في نص مقدس (قرآن/حديث)؟
* *القاعدة:* إذا كانت الإجابة نعم، طَبّق *سياق الآية*.
    * *مثال:* "السفينة" دائمًا تعني "النجاة/السلامة" (إشارة إلى نوح عليه السلام).

### الخطوة 3: التجريد الوظيفي
**السؤال:** ماذا *يفعل* هذا الشيء؟
* *القاعدة:* حوّل الشيء إلى فعل.
    * *القلم* -> يسجل/يحكم -> التفسير: قاضٍ أو حاكم.
    * *المفتاح* -> يفتح/يغلق -> التفسير: الوصول إلى المال أو استجابة الدعاء.

### الخطوة 4: المرشح السياقي (مبادئ السياق)
طبق متغيرات الرائي الخاصة على المعنى الأساسي المستمد أعلاه:

| المتغير | المعدل المنطقي | مثال (الرمز: النار) |
| :--- | :--- | :--- |
| **المهنة** | هل يساعد الرمز عمله أم يعيقه؟ | **الحداد:** ربح/نجاح. <br> **المزارع:** هلاك/قحط. |
| **الصحة** | هل الرائي ضعيف جسديًا؟ | **صحيح:** قوة/طاقة. <br> **مريض:** حمى/موت. |
| **الموسم** | هل الرمز مناسب للوقت؟ | **المطر (شتاءً):** رحمة/خصب. <br> **المطر (صيفًا):** مرض/تعطيل. |
| **الحالة الاجتماعية** | هل الرائي أعزب أم متزوج؟ | **الثوب:** زواج (للأعزب). <br> **الثوب:** جاه/مال (للمتزوج). |

---

## المرحلة الثالثة: التطبيق الحديث والتركيب

تطبيق محرك ابن سيرين السيميائي على القرن الحادي والعشرين.

### 1. الهاتف الذكي (Smartphone)
* **لغوي/وظيفي:** ينقل الأصوات (هاتف) ويحفظ الأسرار. يصل البعيد (صلة).
* **المنهجية:**
    * *الجذر:* "هتف" (صوت من الغيب).
    * *الوظيفة:* اتصال، علم، أرشيف.
* **التفسير:**
    * **عام:** "رسول" أو "ناقل أخبار". يمثل اتصال الرائي بالعالم.
    * **شاشة مكسورة:** صدع في العلاقات أو "سؤء تفاهم" (تشوه الرسالة).
    * **الفقدان:** قطع للرحم أو كشف للأسرار (فضيحة).
    * **للأعزب:** أخبار سارة عن خطبة (هاتف).

### 2. الطائرة
* **القياس:** "سفينة" السماء.
* **المنهجية:**
    * *التوازي الشرعي:* "وخلقنا لهم من مثله ما يركبون".
    * *الوظيفة:* صعود سريع، سفر، نقل.
* **التفسير:**
    * **الصعود:** ارتفاع سريع في المكانة الاجتماعية أو الرتبة الروحية (إشارة: المعراج/الرقي).
    * **الهبوط:** استقرار بعد فترة من التقلب.
    * **التحطم:** سقوط مفاجئ وكارثي من النعمة أو فشل طموح كبير.
    * **للمريض:** رحلة إلى الدار الآخرة (الصعود نحو السماء).

### 3. العملة الرقمية / المحفظة الرقمية
* **القياس:** مال "باطن" (خفي) أو "وديعة".
* **الوظيفة:** قيمة غير مرئية، متقلبة، مشفرة (مختومة).
* **التفسير:**
    * **المحفظة:** علم باطن أو "كنوز مخفية".
    * **فقدان المفتاح:** خيانة أمانة أو نسيان شهادة حاسمة.
    * **التعدين:** بذل جهد في "العلم" الذي يثمر "مالاً".

### 4. التركيب السردي المعقد
**الحلم:** *رائي يحلم أنه يقود طائرة ليلاً باستخدام هاتف ذكي كجهاز تحكم، لكن البطارية تنفد.*

* **التفكيك:**
    * **الطيران (ليلاً):** رحلة غامضة/غير واضحة أو طموح روحي يكتنفه الغموض.
    * **تحكم الهاتف:** الرائي يوجه حياته عبر "الأخبار/المعلومات" أو "العلاقات الاجتماعية".
    * **نفاذ البطارية:** نفاذ "الطاقة" أو "قوة الحياة". فقدان القدرة.
* **التركيب:** الرائي يحاول صعودًا سريعًا وعالي المخاطر في مسيرته المهنية أو مكانته معتمدًا بشكل كبير على *النفوذ الاجتماعي* أو *المعلومات* (الهاتف) بدلاً من الأسس المتينة. "نفاذ البطارية" ينذر بأن *موارده/طاقته* (أو صبر علاقاته) على وشك النفاذ، مما سيؤدي إلى فقدان السيطرة قبل الوصول إلى الوجهة.

        **المهمة:**
        فسر الحلم التالي: "${dream}"

        **شروط الإجابة:**
        - ابدأ بتفسير مباشر وحكيم مستخدماً المنهجية أعلاه.
        - استشهد بالجذور اللغوية أو الشواهد الشرعية عند الحاجة.
        - كن موجزاً وعميقاً.
        - حافظ على نبرة مطمئنة.
        - اختم بعبارة: "والله أعلم".
        `;

        let prompt = englishMethodology;
        if (language === 'ar') {
            prompt = arabicMethodology;
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
