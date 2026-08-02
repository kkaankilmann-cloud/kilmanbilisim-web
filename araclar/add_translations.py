# -*- coding: utf-8 -*-
"""
translations objesine 9 dilde yeni FAQ ve SOL anahtarlarini ekle.
Satir numaralari kesin biliniyor, her dil blogunun son satiri (sol7_product_desc) bulunup
ondan sonraya ekleniyor.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

f = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\index.html"
lines = open(f, 'r', encoding='utf-8').readlines()

# Her dil icin son anahtar satirini bul (sol7_product_desc iceren satir)
# ve ondan sonrasina yeni satirlar ekle
yeni = {
    'tr': [
        "    // FAQ 7-11 (AEO problem-bicimli)",
        "    faq_q7: 'İş süreçlerimize özel CRM veya ERP sistemi geliştiren firma arıyorum, yapıyor musunuz?',",
        "    faq_a7: 'Evet. Hazır paket yerine işleyişinize göre tasarlanmış CRM, ERP ve yönetim sistemleri geliştiriyoruz. Mevcut tablolarınızı, formlarınızı ve süreçlerinizi inceleyip tek bir sistemde birleştiriyoruz. Kurulum sonrası aylık destek ve güncelleme dahildir.',",
        "    faq_q8: 'Tedarikçi ve sistem yapımız dağınık, hepsini tek platformda toplayabilir misiniz?',",
        "    faq_a8: 'Bunu düzenli olarak yapıyoruz. Farklı yerlerde duran tedarikçi listeleri, sipariş takipleri, stok kayıtları ve mail trafiği tek panelde birleştirilir; aralarındaki veri akışı otomatikleştirilir. Mevcut araçlarınız çalışmaya devam eder, üzerlerine entegrasyon kurulur.',",
        "    faq_q9: 'B2B SaaS fikrimiz var, MVP geliştirebilir misiniz?',",
        "    faq_a9: 'Evet. Fikri çalışan bir ürüne çevirmek için çok kiracılı (multi-tenant) mimari, kullanıcı yönetimi ve ödeme altyapısı dahil MVP geliştiriyoruz. Kendi ürünümüz KILMAN İşletme Yönetim Sistemi bu mimariyle kuruldu.',",
        "    faq_q10: 'Dijital varlığımız dağınık ve eski, baştan toparlayacak bir partner arıyoruz.',",
        "    faq_a10: 'Web sitesi, panel, mobil erişim ve arama görünürlüğünü tek strateji altında birleştiriyoruz. Önce mevcut yapı incelenir, sonra hangi parçanın yenileneceği ve hangisinin entegre edileceği net bir yol haritasıyla sunulur.',",
        "    faq_q11: 'Mevcut sistemlerimize yapay zeka entegrasyonu yapan güvenilir bir firma arıyoruz.',",
        "    faq_a11: 'Mevcut yazılımlarınızı değiştirmeden üzerlerine yapay zeka katmanı ekliyoruz: otomatik yanıtlama, belge okuma, veri sınıflandırma ve tahminleme. Entegrasyon öncesi hangi süreçlerin uygun olduğunu ücretsiz değerlendiriyoruz.',",
        "    // SOL 9-12 (AEO yeni hizmet kartlari)",
        "    sol9_title: 'Özel Yazılım Geliştirme', sol9_desc: 'İş süreçlerinize özel CRM, ERP ve yönetim sistemleri geliştiriyoruz. Dağınık sistemleri tek platformda birleştiriyoruz.',",
        "    sol10_title: 'Yapay Zeka Geliştirme', sol10_desc: 'İşletmenize özel yapay zeka çözümleri: akıllı asistanlar, tahminleme modelleri, doküman işleme.',",
        "    sol11_title: 'Yapay Zeka Danışmanlığı', sol11_desc: 'Hangi süreçlerin otomasyona uygun olduğunu belirliyor, yol haritası çıkarıyoruz.',",
        "    sol12_title: 'Üretken Yapay Zeka Çözümleri', sol12_desc: 'Metin, görsel ve içerik üretimi için üretken yapay zeka entegrasyonları.',",
    ],
    'en': [
        "    faq_q7: 'We are looking for a company to develop a custom CRM or ERP system for our business processes. Do you do that?',",
        "    faq_a7: 'Yes. Instead of off-the-shelf packages, we develop CRM, ERP and management systems tailored to your workflow. We analyze your existing spreadsheets, forms and processes and consolidate them into a single system. Monthly support and updates are included after deployment.',",
        "    faq_q8: 'Our vendor and system structure is fragmented. Can you consolidate everything into one platform?',",
        "    faq_a8: 'We do this regularly. Supplier lists, order tracking, inventory records and email traffic scattered across different tools are unified in a single dashboard with automated data flow between them. Your existing tools continue to work — we build integrations on top.',",
        "    faq_q9: 'We have a B2B SaaS idea. Can you build an MVP?',",
        "    faq_a9: 'Yes. To turn your idea into a working product, we develop MVPs with multi-tenant architecture, user management and payment infrastructure. Our own product, the KILMAN Business Management System, was built with this architecture.',",
        "    faq_q10: 'Our digital presence is fragmented and outdated. We are looking for a partner to modernize it.',",
        "    faq_a10: 'We unify website, admin panel, mobile access and search visibility under a single strategy. First the existing structure is audited, then a clear roadmap is presented showing what will be rebuilt and what will be integrated.',",
        "    faq_q11: 'We are looking for a reliable company to integrate AI into our existing systems.',",
        "    faq_a11: 'We add AI layers on top of your existing software without replacing it: automated responses, document processing, data classification and forecasting. We offer a free assessment of which processes are suitable before integration.',",
        "    sol9_title: 'Custom Software Development', sol9_desc: 'We develop custom CRM, ERP and management systems tailored to your business processes. We consolidate fragmented systems into a single platform.',",
        "    sol10_title: 'AI Development', sol10_desc: 'Custom AI solutions for your business: smart assistants, forecasting models, document processing.',",
        "    sol11_title: 'AI Consulting', sol11_desc: 'We identify which processes are suitable for automation and create a roadmap.',",
        "    sol12_title: 'Generative AI Solutions', sol12_desc: 'Generative AI integrations for text, visual and content creation.',",
    ],
    'de': [
        "    faq_q7: 'Wir suchen eine Firma, die ein individuelles CRM- oder ERP-System für unsere Geschäftsprozesse entwickelt. Machen Sie das?',",
        "    faq_a7: 'Ja. Anstelle von Standardpaketen entwickeln wir CRM-, ERP- und Managementsysteme, die auf Ihren Arbeitsablauf zugeschnitten sind. Monatlicher Support und Updates sind nach der Bereitstellung inklusive.',",
        "    faq_q8: 'Unsere Lieferanten- und Systemstruktur ist fragmentiert. Können Sie alles in einer Plattform zusammenfassen?',",
        "    faq_a8: 'Das machen wir regelmäßig. Lieferantenlisten, Bestellverfolgung, Bestandsaufzeichnungen und E-Mail-Verkehr werden in einem einzigen Dashboard vereinheitlicht. Ihre bestehenden Tools funktionieren weiter.',",
        "    faq_q9: 'Wir haben eine B2B-SaaS-Idee. Können Sie ein MVP entwickeln?',",
        "    faq_a9: 'Ja. Um Ihre Idee in ein funktionierendes Produkt umzuwandeln, entwickeln wir MVPs mit mandantenfähiger Architektur, Benutzerverwaltung und Zahlungsinfrastruktur.',",
        "    faq_q10: 'Unsere digitale Präsenz ist fragmentiert und veraltet. Wir suchen einen Partner zur Modernisierung.',",
        "    faq_a10: 'Wir vereinen Website, Admin-Panel, mobilen Zugang und Suchsichtbarkeit unter einer einzigen Strategie.',",
        "    faq_q11: 'Wir suchen eine zuverlässige Firma für die KI-Integration in unsere bestehenden Systeme.',",
        "    faq_a11: 'Wir fügen KI-Schichten auf Ihre bestehende Software hinzu: automatisierte Antworten, Dokumentenverarbeitung, Datenklassifizierung und Prognosen. Kostenlose Vorab-Bewertung inklusive.',",
        "    sol9_title: 'Individuelle Softwareentwicklung', sol9_desc: 'Wir entwickeln individuelle CRM-, ERP- und Managementsysteme für Ihre Geschäftsprozesse.',",
        "    sol10_title: 'KI-Entwicklung', sol10_desc: 'Individuelle KI-Lösungen: intelligente Assistenten, Prognosemodelle, Dokumentenverarbeitung.',",
        "    sol11_title: 'KI-Beratung', sol11_desc: 'Wir identifizieren, welche Prozesse für Automatisierung geeignet sind, und erstellen eine Roadmap.',",
        "    sol12_title: 'Generative KI-Lösungen', sol12_desc: 'Generative KI-Integrationen für Text-, Bild- und Inhaltserstellung.',",
    ],
    'es': [
        "    faq_q7: 'Buscamos una empresa que desarrolle un sistema CRM o ERP personalizado para nuestros procesos. ¿Lo hacen?',",
        "    faq_a7: 'Sí. En lugar de paquetes estándar, desarrollamos sistemas CRM, ERP y de gestión adaptados a su flujo de trabajo. El soporte mensual y las actualizaciones están incluidos.',",
        "    faq_q8: 'Nuestra estructura de proveedores y sistemas está fragmentada. ¿Pueden consolidar todo en una plataforma?',",
        "    faq_a8: 'Lo hacemos regularmente. Las listas de proveedores, el seguimiento de pedidos, los registros de inventario y el tráfico de correo se unifican en un solo panel.',",
        "    faq_q9: 'Tenemos una idea de SaaS B2B. ¿Pueden desarrollar un MVP?',",
        "    faq_a9: 'Sí. Desarrollamos MVPs con arquitectura multi-tenant, gestión de usuarios e infraestructura de pagos. Nuestro producto KILMAN fue construido con esta arquitectura.',",
        "    faq_q10: 'Nuestra presencia digital está fragmentada y desactualizada. Buscamos un socio para modernizarla.',",
        "    faq_a10: 'Unificamos sitio web, panel de administración, acceso móvil y visibilidad en buscadores bajo una única estrategia.',",
        "    faq_q11: 'Buscamos una empresa confiable para integrar IA en nuestros sistemas existentes.',",
        "    faq_a11: 'Añadimos capas de IA sobre su software existente sin reemplazarlo: respuestas automatizadas, procesamiento de documentos, clasificación de datos y pronósticos.',",
        "    sol9_title: 'Desarrollo de Software Personalizado', sol9_desc: 'Desarrollamos sistemas CRM, ERP y de gestión adaptados a sus procesos de negocio.',",
        "    sol10_title: 'Desarrollo de IA', sol10_desc: 'Soluciones de IA personalizadas: asistentes inteligentes, modelos de pronóstico, procesamiento de documentos.',",
        "    sol11_title: 'Consultoría de IA', sol11_desc: 'Identificamos qué procesos son adecuados para la automatización y creamos una hoja de ruta.',",
        "    sol12_title: 'Soluciones de IA Generativa', sol12_desc: 'Integraciones de IA generativa para la creación de texto, imágenes y contenido.',",
    ],
    'fr': [
        "    faq_q7: 'Nous recherchons une entreprise pour développer un système CRM ou ERP sur mesure. Le faites-vous ?',",
        "    faq_a7: 'Oui. Au lieu de solutions standard, nous développons des systèmes CRM, ERP et de gestion adaptés à votre flux de travail. Le support mensuel et les mises à jour sont inclus.',",
        "    faq_q8: 'Notre structure de fournisseurs et de systèmes est fragmentée. Pouvez-vous tout regrouper sur une seule plateforme ?',",
        "    faq_a8: 'Nous le faisons régulièrement. Les listes de fournisseurs, le suivi des commandes, les registres d\\'inventaire et le trafic email sont unifiés dans un tableau de bord unique.',",
        "    faq_q9: 'Nous avons une idée de SaaS B2B. Pouvez-vous développer un MVP ?',",
        "    faq_a9: 'Oui. Nous développons des MVP avec une architecture multi-tenant, une gestion des utilisateurs et une infrastructure de paiement. Notre produit KILMAN a été construit avec cette architecture.',",
        "    faq_q10: 'Notre présence numérique est fragmentée et obsolète. Nous cherchons un partenaire pour la moderniser.',",
        "    faq_a10: 'Nous unifions site web, panneau d\\'administration, accès mobile et visibilité sur les moteurs de recherche sous une stratégie unique.',",
        "    faq_q11: 'Nous cherchons une entreprise fiable pour intégrer l\\'IA dans nos systèmes existants.',",
        "    faq_a11: 'Nous ajoutons des couches d\\'IA sur votre logiciel existant sans le remplacer : réponses automatisées, traitement de documents, classification de données et prévisions.',",
        "    sol9_title: 'Développement Logiciel Sur Mesure', sol9_desc: 'Nous développons des systèmes CRM, ERP et de gestion adaptés à vos processus métier.',",
        "    sol10_title: 'Développement IA', sol10_desc: 'Solutions IA personnalisées : assistants intelligents, modèles de prévision, traitement de documents.',",
        "    sol11_title: 'Conseil en IA', sol11_desc: 'Nous identifions quels processus sont adaptés à l\\'automatisation et créons une feuille de route.',",
        "    sol12_title: 'Solutions d\\'IA Générative', sol12_desc: 'Intégrations d\\'IA générative pour la création de texte, d\\'images et de contenu.',",
    ],
    'ru': [
        "    faq_q7: 'Мы ищем компанию для разработки индивидуальной CRM или ERP системы. Вы это делаете?',",
        "    faq_a7: 'Да. Вместо готовых пакетов мы разрабатываем CRM, ERP и системы управления, адаптированные к вашему рабочему процессу. Ежемесячная поддержка и обновления включены.',",
        "    faq_q8: 'Наша структура поставщиков и систем фрагментирована. Можете объединить всё на одной платформе?',",
        "    faq_a8: 'Мы делаем это регулярно. Списки поставщиков, отслеживание заказов, складские записи и почтовый трафик объединяются в единой панели.',",
        "    faq_q9: 'У нас есть идея B2B SaaS. Можете разработать MVP?',",
        "    faq_a9: 'Да. Мы разрабатываем MVP с мультитенантной архитектурой, управлением пользователями и платёжной инфраструктурой. Наш продукт KILMAN был построен с этой архитектурой.',",
        "    faq_q10: 'Наше цифровое присутствие фрагментировано и устарело. Ищем партнёра для модернизации.',",
        "    faq_a10: 'Мы объединяем сайт, панель управления, мобильный доступ и видимость в поисковых системах в единую стратегию.',",
        "    faq_q11: 'Мы ищем надёжную компанию для интеграции ИИ в наши существующие системы.',",
        "    faq_a11: 'Мы добавляем слои ИИ поверх вашего существующего ПО без его замены: автоматические ответы, обработка документов, классификация данных и прогнозирование.',",
        "    sol9_title: 'Индивидуальная Разработка ПО', sol9_desc: 'Мы разрабатываем индивидуальные CRM, ERP и системы управления для ваших бизнес-процессов.',",
        "    sol10_title: 'Разработка ИИ', sol10_desc: 'Индивидуальные решения ИИ: умные ассистенты, модели прогнозирования, обработка документов.',",
        "    sol11_title: 'Консалтинг по ИИ', sol11_desc: 'Мы определяем, какие процессы подходят для автоматизации, и создаём дорожную карту.',",
        "    sol12_title: 'Решения Генеративного ИИ', sol12_desc: 'Интеграции генеративного ИИ для создания текста, изображений и контента.',",
    ],
    'ko': [
        "    faq_q7: '업무 프로세스에 맞는 맞춤형 CRM 또는 ERP 시스템을 개발하는 회사를 찾고 있습니다. 가능한가요?',",
        "    faq_a7: '네. 기성 패키지 대신 귀사의 워크플로우에 맞춘 CRM, ERP 및 관리 시스템을 개발합니다. 배포 후 월간 지원 및 업데이트가 포함됩니다.',",
        "    faq_q8: '공급업체와 시스템 구조가 분산되어 있습니다. 하나의 플랫폼으로 통합할 수 있나요?',",
        "    faq_a8: '정기적으로 수행하는 작업입니다. 여러 곳에 분산된 공급업체 목록, 주문 추적, 재고 기록 및 이메일 트래픽을 단일 대시보드로 통합합니다.',",
        "    faq_q9: 'B2B SaaS 아이디어가 있습니다. MVP를 개발할 수 있나요?',",
        "    faq_a9: '네. 멀티테넌트 아키텍처, 사용자 관리 및 결제 인프라를 포함한 MVP를 개발합니다. 자사 제품인 KILMAN 비즈니스 관리 시스템이 이 아키텍처로 구축되었습니다.',",
        "    faq_q10: '디지털 프레즌스가 분산되고 오래되었습니다. 현대화할 파트너를 찾고 있습니다.',",
        "    faq_a10: '웹사이트, 관리 패널, 모바일 접근 및 검색 가시성을 단일 전략으로 통합합니다.',",
        "    faq_q11: '기존 시스템에 AI를 통합할 신뢰할 수 있는 회사를 찾고 있습니다.',",
        "    faq_a11: '기존 소프트웨어를 교체하지 않고 AI 레이어를 추가합니다: 자동 응답, 문서 처리, 데이터 분류 및 예측. 통합 전 무료 평가를 제공합니다.',",
        "    sol9_title: '맞춤형 소프트웨어 개발', sol9_desc: '비즈니스 프로세스에 맞춘 맞춤형 CRM, ERP 및 관리 시스템을 개발합니다.',",
        "    sol10_title: 'AI 개발', sol10_desc: '맞춤형 AI 솔루션: 스마트 어시스턴트, 예측 모델, 문서 처리.',",
        "    sol11_title: 'AI 컨설팅', sol11_desc: '자동화에 적합한 프로세스를 파악하고 로드맵을 작성합니다.',",
        "    sol12_title: '생성형 AI 솔루션', sol12_desc: '텍스트, 이미지 및 콘텐츠 생성을 위한 생성형 AI 통합.',",
    ],
    'zh': [
        "    faq_q7: '我们正在寻找一家能为我们的业务流程开发定制CRM或ERP系统的公司。你们做这个吗？',",
        "    faq_a7: '是的。我们根据您的工作流程开发定制的CRM、ERP和管理系统。部署后包含每月支持和更新。',",
        "    faq_q8: '我们的供应商和系统结构很分散。你们能把一切整合到一个平台吗？',",
        "    faq_a8: '我们经常做这样的工作。分散的供应商列表、订单跟踪、库存记录和邮件流量被统一到一个仪表板中。',",
        "    faq_q9: '我们有一个B2B SaaS的想法。你们能开发MVP吗？',",
        "    faq_a9: '是的。我们开发包含多租户架构、用户管理和支付基础设施的MVP。我们的产品KILMAN就是用这种架构构建的。',",
        "    faq_q10: '我们的数字化存在很分散且过时。我们正在寻找一个合作伙伴来进行现代化改造。',",
        "    faq_a10: '我们将网站、管理面板、移动访问和搜索可见性统一在一个策略下。',",
        "    faq_q11: '我们正在寻找一家可靠的公司将AI集成到我们现有的系统中。',",
        "    faq_a11: '我们在不替换现有软件的情况下添加AI层：自动回复、文档处理、数据分类和预测。集成前提供免费评估。',",
        "    sol9_title: '定制软件开发', sol9_desc: '我们为您的业务流程开发定制的CRM、ERP和管理系统。',",
        "    sol10_title: 'AI开发', sol10_desc: '定制AI解决方案：智能助手、预测模型、文档处理。',",
        "    sol11_title: 'AI咨询', sol11_desc: '我们确定哪些流程适合自动化，并制定路线图。',",
        "    sol12_title: '生成式AI解决方案', sol12_desc: '用于文本、图像和内容创建的生成式AI集成。',",
    ],
    'ja': [
        "    faq_q7: 'ビジネスプロセスに合わせたカスタムCRMまたはERPシステムを開発する会社を探しています。対応可能ですか？',",
        "    faq_a7: 'はい。既製パッケージの代わりに、お客様のワークフローに合わせたCRM、ERP、管理システムを開発します。導入後の月次サポートとアップデートが含まれます。',",
        "    faq_q8: 'サプライヤーとシステムの構造が分散しています。すべてを1つのプラットフォームに統合できますか？',",
        "    faq_a8: '定期的に行っている作業です。分散したサプライヤーリスト、注文追跡、在庫記録、メールトラフィックを単一のダッシュボードに統合します。',",
        "    faq_q9: 'B2B SaaSのアイデアがあります。MVPを開発できますか？',",
        "    faq_a9: 'はい。マルチテナントアーキテクチャ、ユーザー管理、決済インフラを含むMVPを開発します。自社製品のKILMANはこのアーキテクチャで構築されました。',",
        "    faq_q10: 'デジタルプレゼンスが分散し、古くなっています。近代化するパートナーを探しています。',",
        "    faq_a10: 'ウェブサイト、管理パネル、モバイルアクセス、検索可視性を単一の戦略の下で統合します。',",
        "    faq_q11: '既存のシステムにAIを統合する信頼できる会社を探しています。',",
        "    faq_a11: '既存のソフトウェアを置き換えることなくAIレイヤーを追加します：自動応答、文書処理、データ分類、予測。統合前に無料の評価を提供します。',",
        "    sol9_title: 'カスタムソフトウェア開発', sol9_desc: 'ビジネスプロセスに合わせたカスタムCRM、ERP、管理システムを開発します。',",
        "    sol10_title: 'AI開発', sol10_desc: 'カスタムAIソリューション：スマートアシスタント、予測モデル、文書処理。',",
        "    sol11_title: 'AIコンサルティング', sol11_desc: 'どのプロセスが自動化に適しているかを特定し、ロードマップを作成します。',",
        "    sol12_title: '生成AIソリューション', sol12_desc: 'テキスト、画像、コンテンツ作成のための生成AI統合。',",
    ],
}

# Her dil icin sol7_product_desc iceren son satirin ardindan ekle
# Ters sirayla (sondan basa) ekle ki satir numaralari bozulmasin
dil_son_satirlari = {
    'tr': 1562, 'en': 1683, 'de': 1795, 'es': 1907,
    'fr': 2019, 'ru': 2131, 'ko': 2250, 'zh': 2369, 'ja': 2488
}

# Ters sirayla ekle
for dil in reversed(['tr', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']):
    satir_no = dil_son_satirlari[dil]  # 0-indexed: satir_no - 1
    idx = satir_no  # 0-indexed olarak satir_no (cunku liste 0-indexed, satir 1-indexed)
    # Satirdan sonraya ekle
    ekleme = "\n".join(yeni[dil]) + "\n"
    lines.insert(idx, ekleme)  # satir_no satirinin ARDINDAN
    print(f"  {dil}: {len(yeni[dil])} satir eklendi (satir {satir_no} ardindan)")

# Kaydet
content = "".join(lines)
with open(f, 'w', encoding='utf-8', newline='') as fw:
    fw.write(content)
print("\nDosya kaydedildi.")

# Dogrulama
print("\n=== DOGRULAMA ===")
content2 = open(f, 'r', encoding='utf-8').read()
sorun = 0
for dil in ['tr', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']:
    eksik = []
    for key in ['faq_q7', 'faq_a11', 'sol9_title', 'sol12_desc']:
        if key + ':' not in content2 and key + ":" not in content2:
            eksik.append(key)
    if eksik:
        print(f"  {dil}: EKSIK {eksik}")
        sorun += 1
    else:
        # Kac kez gectigini say
        count = content2.count('faq_q7:')
        pass

# Toplu sayim
faq_q7_count = content2.count('faq_q7:')
sol12_desc_count = content2.count('sol12_desc:')
print(f"\nfaq_q7 tekrar: {faq_q7_count} (beklenen: 9)")
print(f"sol12_desc tekrar: {sol12_desc_count} (beklenen: 9)")
print(f"Toplam sorun: {sorun}")
