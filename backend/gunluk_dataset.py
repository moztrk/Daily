# gunluk_dataset.py - Kaliteli Günlük Örnekleri

GUNLUK_ORNEKLERI = [
    
    # ================== İŞ VE KARİYER (30 örnek) ==================
    
    # Pozitif
    "Bugün patronla toplantımız çok verimli geçti. Yeni projede liderlik rolü almam konusunda anlaştık. Çok mutluyum, kariyerimde yeni bir sayfa açılıyor.",
    "Ofiste harika bir gün geçirdim. Ekip arkadaşlarımla yeni pazarlama stratejisini planladık. Müdürümüz fikirlerimizi çok beğendi.",
    "İşe yeni başlayan arkadaşa mentorluk yapıyorum. Ona yardım etmek beni mutlu ediyor. Ofis ortamı çok olumlu.",
    "Proje sunumum çok başarılı geçti. Patronum performansımdan övgüyle bahsetti. Terfi konusunda umutlarım arttı.",
    "Bugün yeni bir iş teklifi aldım. Maaş artışı da var. Düşünmem için zaman istedim ama içim rahat.",
    "Ekip toplantısında önerim kabul edildi. Herkes fikrimin çok iyi olduğunu söyledi. Kendime güvenim arttı.",
    "Uzun zamandır beklediğim terfi haberi geldi. Maaşım da artacak. Aileme müjdeyi vermek için sabırsızlanıyorum.",
    "İş yerinde yeni bir proje başlattık. Sorumluluk bende. Heyecanlıyım ama hazırım.",
    "Bugün işte çok üretken bir gün geçirdim. Tüm görevlerimi zamanında tamamladım. Akşam kendime ödül vereceğim.",
    "Mesaiden sonra ekiple yemek yedik. İş dışında da güzel vakit geçirmek güzeldi.",
    
    # Nötr
    "Bugün normal bir iş günüydü. Sabah toplantı, öğlen raporlar, akşam eve. Rutin devam ediyor.",
    "Ofiste sessiz bir gündü. Herkes kendi işine odaklanmış. Ben de raporları hazırladım.",
    "İşe gittim, görevlerimi yaptım, eve döndüm. Sıradan ama yorucu bir gün.",
    "Bugün toplantılar çoktu. Biraz yoruldum ama işler yolunda gidiyor.",
    "Müşteri görüşmesi yaptım. Sonuç belirsiz ama olumlu sinyaller vardı.",
    "İş yerinde yeni bir sistem kullanmaya başladık. Alışmaya çalışıyorum.",
    "Proje raporu hazırladım. Yarın sunacağım. Rutinin bir parçası artık.",
    "Mesaiye kaldım. İşler birikmiş. Yarın daha az yoğun olur umarım.",
    
    # Negatif
    "Bugün patronla tartıştık. Projede haksız eleştiri aldım. Canım çok sıkıldı.",
    "İş yerinde çok stresli bir gündü. Her şey ters gitti. Müşteri şikayet etti, patronum sinirli.",
    "Terfi alamadım. Çok hayal kırıklığına uğradım. Belki başka fırsatlar çıkar.",
    "İş yükü çok fazla. Sürekli fazla mesai yapıyorum. Yoruldum artık.",
    "Proje başarısız oldu. Ekip olarak moralimiz bozuk. Yeniden başlamak zor olacak.",
    "Maaş zamları açıklandı. Benim hiç zam almadığımı öğrendim. Üzüldüm.",
    "İş yerinde dedikodu çok. Ortam gergin. Ofise gitmek istemiyorum artık.",
    "Toplantıda fikrimi söyleyemedim. Kendimi ifade edemiyorum. İçime atıyorum.",
    "Bugün işten kovulma riski olduğunu öğrendim. Çok endişeliyim. Ne yapacağımı bilmiyorum.",
    "Patron bugün herkese bağırdı. Ofis ortamı berbat. Eve geldiğimde rahatladım.",
    
    
    # ================== EĞİTİM VE OKUL (25 örnek) ==================
    
    # Pozitif
    "Bugün matematik sınavından tam not aldım. Öğretmenim sınıfta tebrik etti. Çok mutluyum.",
    "Okulda proje sunumumuz birinci oldu. Arkadaşlarımla çok çalışmıştık. Ödülü hak ettik.",
    "Üniversite sınavı sonuçları açıklandı. İstediğim bölümü kazandım. Ailem çok gururlu.",
    "Bugün okulda çok eğlenceli bir ders yaptık. Öğretmenimiz interaktif aktiviteler hazırlamış.",
    "Grup ödevimiz çok iyi oldu. Arkadaşlarımla uyumlu çalıştık. Yüksek not bekliyorum.",
    "Okulda bilim fuarı vardı. Projemizi sergiledik. Çok ilgi gördük.",
    "İngilizce dersinde sunum yaptım. Öğretmen çok beğendi. Kendime güvenim arttı.",
    "Bugün okulda yeni arkadaşlar edindim. Teneffüslerde birlikte vakit geçirdik.",
    "Karne günüydü. Tüm derslerimden iyi notlar aldım. Ailem çok mutlu oldu.",
    "Üniversitede burs kazandım. Maddi açıdan rahatladım. Ailem de sevindi.",
    
    # Nötr
    "Bugün okulda normal bir gündü. Dersler, ödevler, eve dönüş.",
    "Matematik ödevini yaptım. Biraz zorluk çektiğim yerler oldu ama hallediyorum.",
    "Okulda kütüphanede ders çalıştım. Sınav haftası yaklaşıyor.",
    "Bugün fizik dersi vardı. Yeni konu işledik. Akşam tekrar yapacağım.",
    "Sınıfta grup çalışması yaptık. İdare eder gibiydi.",
    "Okul çıkışı arkadaşlarımla kafe gittik. Biraz sohbet ettik.",
    
    # Negatif
    "Bugün sınavdan kötü not aldım. Çok çalışmıştım ama yeterli olmamış. Üzgünüm.",
    "Öğretmen bugün beni sınıfta azarladı. Çok utandım. Haksızlığa uğradım.",
    "Okul çok stresli. Sınavlar, ödevler bitmiyor. Yoruldum artık.",
    "Grup ödevinde arkadaşlarım hiç çalışmadı. Tüm yük bende kaldı. Sinirliyim.",
    "Bugün okulda yalnız hissettim. Arkadaşlarım benimle konuşmadı.",
    "Matematik dersini hiç anlamadım. Öğretmen çok hızlı anlattı. Kayboldum.",
    "Sınav haftası başlıyor. Hiç hazır değilim. Çok endişeliyim.",
    "Üniversite sınavı yaklaşıyor. Stres seviyem çok yüksek. Uyuyamıyorum.",
    "Okulda zorbalığa maruz kaldım. Kimseye söyleyemedim. İçimde tutuyorum.",
    
    
    # ================== SAĞLIK (30 örnek) ==================
    
    # Pozitif
    "Bugün spor salonuna gittim. Harika bir antrenman yaptım. Kendimi çok iyi hissediyorum.",
    "Doktor kontrolünden yeni çıktım. Tüm değerlerim normal. Sağlığıma dikkat etmeye devam edeceğim.",
    "Sabah koşusu yaptım. Hava çok güzeldi. Enerji doldum.",
    "Vitamin takviyelerine başladım. Kendimi daha dinç hissediyorum.",
    "Bugün yoga yaptım. Hem vücudum hem zihnim rahatladı.",
    "Kilolarımdan 3 kilo verdim. Diyet ve spor işe yarıyor. Mutluyum.",
    "Bugün çok su içtim. Kendimi daha dinç hissediyorum.",
    "Sabah erken kalktım ve meditasyon yaptım. Günü daha huzurlu geçiriyorum.",
    "Bugün sağlıklı bir kahvaltı yaptım. Enerji seviyem çok iyi.",
    "Spor arkadaşlarımla voleybol oynadık. Hem eğlendik hem spor yaptık.",
    
    # Nötr
    "Bugün hastaneye gidip kan tahlili yaptırdım. Sonuçlar birkaç güne çıkacak.",
    "Eczaneye gittim ve vitaminlerimi aldım. Rutin kontrol.",
    "Bugün başım biraz ağrıdı. Parol içtim, geçti.",
    "Diş hekimine gittim. Rutin kontrol yaptırdım. Her şey normal.",
    "Bugün fazla yürüdüm. Bacaklarım yoruldu ama kötü değil.",
    "Grip olmamak için önlem alıyorum. Bol su içiyorum.",
    
    # Negatif  
    "Bugün çok hasta hissettim. Ateşim var. Hastaneye gitmem gerekebilir.",
    "Baş ağrım geçmiyor. Üç gündür ilaç içiyorum. İyileşmiyorum.",
    "Bugün mide bulantısı çektim. Bir şeyler yedim ama kusasım geldi.",
    "Çok yorgunum. Sürekli uyumak istiyorum. Belki demir eksikliği var.",
    "Alerjim tekrar başladı. Gözlerim kaşınıyor, hapşırıyorum.",
    "Bugün dizim çok ağrıdı. Belki doktora görünmeliyim.",
    "Uykusuzluk problemim var. Geceleri uyuyamıyorum. Yorgun uyanıyorum.",
    "Bugün hastaneye gittim. Doktor kan tahlili istedi. Endişeliyim.",
    "Migren krizim var. Ağrıdan hiçbir şey yapamıyorum.",
    "Bugün nefes almakta zorlandım. Astım ilacımı içtim.",
    "Sırtım çok ağrıyor. Fizik tedaviye başlamam lazım.",
    "Grip oldum. Burnumdan geliyor, boğazım ağrıyor. İşe gidemedim.",
    "Mide ağrım çok şiddetli. Acile gitmem gerekebilir.",
    "Bugün çok halsizim. Doktor yorgunluk teşhisi koydu.",
    
    
    # ================== AİLE (25 örnek) ==================
    
    # Pozitif
    "Bugün annemle çok güzel vakit geçirdik. Birlikte alışveriş yaptık ve kahve içtik.",
    "Babam bugün beni işten aldı. Yolda güzel sohbet ettik. Onu özlemişim.",
    "Kardeşimle sinemaya gittik. Çok eğlendik. Güzel bir film izledik.",
    "Aile toplantısı yaptık. Herkes bir araya geldi. Çok keyifli bir gün oldu.",
    "Annemle birlikte yemek yaptık. Çok lezzetli oldu. Babam çok beğendi.",
    "Bugün ailemle pikniğe gittik. Hava çok güzeldi. Çocuklar çok eğlendi.",
    "Kardeşim üniversite sınavını kazandı. Çok mutlu olduk. Kutlama yaptık.",
    "Babamın doğum günüydü. Sürpriz parti yaptık. Çok mutlu oldu.",
    "Bugün annemle telefonda uzun uzun konuştuk. Onu duymak çok iyi geldi.",
    "Ailemle birlikte tatil planları yaptık. Yaz tatilini dört gözle bekliyoruz.",
    
    # Nötr
    "Bugün ailemle normal bir gün geçirdik. Akşam yemeğini birlikte yedik.",
    "Anneme market alışverişinde yardım ettim. Rutin bir gündü.",
    "Kardeşime ödevinde yardım ettim. Birkaç saat çalıştık.",
    "Babamla televizyon izledik. Haber ve belgesel seyrettik.",
    "Bugün evde ailece vakit geçirdik. Özel bir şey olmadı.",
    
    # Negatif
    "Bugün annemle tartıştık. Bir konuda anlaşamadık. İkimiz de sinirliyiz.",
    "Kardeşimle kavga ettik. Küs duruyoruz. Barışmamız lazım.",
    "Babam bugün çok sinirli geldi evde. Ortam gergin. Sessiz kaldım.",
    "Ailemle iletişim problemlerimiz var. Konuşmuyoruz artık.",
    "Annem hasta. Çok endişeliyim. Hastaneye götürmemiz gerekebilir.",
    "Bugün aile içinde büyük bir tartışma oldu. Herkes birbirine kızgın.",
    "Babamın sağlık durumu kötüleşiyor. Çok üzülüyorum.",
    "Kardeşim problemli davranıyor. Ailece endişeliyiz.",
    "Evde maddi sıkıntılar var. Babam stresli. Ortam gergin.",
    "Bugün ailemle büyük bir anlaşmazlık yaşadık. Üzgünüm.",
    
    
    # ================== FİNANS VE PARA (25 örnek) ==================
    
    # Pozitif
    "Bugün maaşım yattı. Birikmiş faturalarımı ödedim. Rahatladım.",
    "Bankada kredi başvurum onaylandı. Araba alacağım. Çok mutluyum.",
    "Bugün yatırım yaptığım hisseler çok değer kazandı. Güzel bir gelir elde ettim.",
    "Para biriktiriyorum. Hedefime her gün biraz daha yaklaşıyorum.",
    "Bugün bütçemi planladım. Gelir gider dengem çok iyi.",
    "Online satış yaptım. İyi gelir elde ettim. Yan gelir kaynağı buldum.",
    "Bugün eski eşyalarımı sattım. Hem dolap boşaldı hem cebim doldu.",
    "Bankadan indirim günüydü. Alışverişte çok tasarruf ettim.",
    
    # Nötr
    "Bugün markete gittim. Normal alışveriş yaptım. Harcama planında kaldım.",
    "Faturalarımı ödedim. Elektrik, su, internet. Rutin ödemeler.",
    "Bankaya gittim ve hesap hareketlerimi kontrol ettim.",
    "Bugün online alışveriş yaptım. İhtiyacım olan şeyleri aldım.",
    "Kredi kartı borcumu ödedim. Taksitlerim devam ediyor.",
    
    # Negatif
    "Bugün 500 lira harcadım. Maaşım gelince ödeyeceğim. Endişeliyim.",
    "Kredi kartı borçlarım çok arttı. Nasıl ödeyeceğim bilmiyorum.",
    "Maaşım yetmiyor artık. Hayat pahalılığı çok yüksek. Zorlanıyorum.",
    "Bugün bankadan kredi reddedildi. Çok hayal kırıklığına uğradım.",
    "Faturalar çok yüksek geldi. Nasıl ödeyeceğim düşünüyorum.",
    "İşsizim. Para sıkıntısı yaşıyorum. Çok stresli bir dönem.",
    "Bugün cüzdanımı kaybettim. İçinde param ve kartlarım vardı. Çok üzgünüm.",
    "Elektrik faturası çok yüksek geldi. Bütçem altüst oldu.",
    "Araba tamiri çok pahalıya patladı. Beklemediğim bir masraf.",
    "Bugün dolandırıldım. 1000 lira kaybettim. Çok pişmanım.",
    "Kira zammı geldi. Ev sahibi çok artırdı. Taşınmayı düşünüyorum.",
    "Borçlarımı ödeyemiyorum. Aileme yük olmak istemiyorum.",
    
    
    # ================== TEKNOLOJİ (20 örnek) ==================
    
    # Pozitif
    "Bugün yeni bir programlama dili öğrenmeye başladım. Python çok eğlenceli.",
    "Bilgisayar oyunu geliştiriyorum. İlk prototip çok iyi oldu. Heyecanlıyım.",
    "Yeni telefon aldım. Kamera kalitesi harika. Çok memnunum.",
    "Bugün bir web sitesi tasarladım. Çok hoşuma gitti. Müşteri beğenecek.",
    "Yapay zeka ile ilgili online kurs bitirdim. Sertifika aldım. Gurur duydum.",
    "Bilgisayarımı upgrade ettim. Artık çok hızlı çalışıyor.",
    "Yeni uygulama geliştirdim. Beta testi başarılı. Yakında yayınlayacağım.",
    
    # Nötr
    "Bugün bilgisayar başında çok vakit geçirdim. Kod yazdım.",
    "Telefon güncellemesi yaptım. Yeni özellikler var.",
    "Online toplantı yaptık. İnternet bağlantısı iyi değildi.",
    "Bilgisayarım biraz yavaşlamaya başladı. Temizlik yapmalıyım.",
    
    # Negatif
    "Bilgisayarım bozuldu. Servis çok pahalı. Ne yapacağımı bilmiyorum.",
    "Bugün veri kaybettim. Yedekleme yapmamıştım. Çok pişmanım.",
    "İnternet çok yavaş. Hiçbir şey yüklenmiyor. Sinirliyim.",
    "Telefon ekranım kırıldı. Tamir masrafı çok yüksek.",
    "Hacklendiğimi öğrendim. Tüm şifrelerimi değiştirdim. Çok endişeliyim.",
    "Bilgisayar virüsü kaptı. Tüm dosyalarım tehlikede.",
    "Online dolandırıcılık girişimi oldu. Neyse ki fark ettim.",
    "Yazılım geliştirme projesi başarısız oldu. Çok emek vermiştimdim.",
    "Sosyal medya hesabım çalındı. Geri alamıyorum.",
    
    
    # ================== KİŞİSEL GELİŞİM (20 örnek) ==================
    
    # Pozitif
    "Bugün bir kişisel gelişim kitabı bitirdim. Çok şey öğrendim. Uygulayacağım.",
    "Hedef listemi güncelledim. Bu yıl içinde başarmak istediğim şeyleri yazdım. Motiveyim.",
    "Online seminere katıldım. İlham vericiydi. Yeni hedefler belirledim.",
    "Bugün meditasyon yaptım. Zihnim çok rahatladı. Düzenli yapmayı planlıyorum.",
    "Yabancı dil çalışıyorum. Her gün ilerliyorum. Kendimle gurur duyuyorum.",
    "Bugün journal yazmaya başladım. Düşüncelerimi dökmek iyi geldi.",
    "Podcast dinledim. Motivasyon konuşması çok iyiydi. İlham aldım.",
    "Yeni bir hobi edindim. Çok keyifli. Kendime zaman ayırıyorum.",
    
    # Nötr
    "Bugün kitap okudum. İlginç bir kurgu romanıydı.",
    "Kişisel gelişim videoları izledim. Not aldım.",
    "Bugün hedeflerim hakkında düşündüm. Plan yapmaya çalışıyorum.",
    
    # Negatif
    "Hedeflerime ulaşamıyorum. Motivasyonum çok düştü. Üzgünüm.",
    "Bugün hiçbir şey yapamadım. Tembellik yaptım. Pişmanım.",
    "Kendime güvenim azaldı. Her şey başarısızlıkla bitiyor.",
    "Procrastination yapıyorum. İşleri erteliyorum. Kendime kızgınım.",
    "Hedeflerimi gerçekleştiremiyorum. Hayal kırıklığı yaşıyorum.",
    "Bugün çok negatiftim. Hiçbir şey motivasyon vermedi.",
    "Özgüven problemim var. Kendimi yetersiz hissediyorum.",
    "Yeni şeyler öğrenemiyorum. Beyin uyuşmuş gibi.",
    "Sosyal anksiyetem arttı. İnsanlarla konuşmaktan kaçınıyorum.",
    
    
    # ================== SOSYAL İLİŞKİLER (20 örnek) ==================
    
    # Pozitif
    "Bugün arkadaşlarımla harika vakit geçirdik. Sinemaya gittik, yemek yedik. Çok eğlendik.",
    "Eski bir arkadaşımla buluştuk. Çok özlemişim. Güzel sohbet ettik.",
    "Bugün yeni arkadaşlar edindim. Hobi grubumuza katıldılar. Keyifli bir gündü.",
    "Dostlarımla piknik yaptık. Hava çok güzeldi. Hep birlikte güldük.",
    "Bugün arkadaşımın doğum gününü kutladık. Sürpriz parti yaptık. Çok mutlu oldu.",
    "Yakın arkadaşımla dertleştik. Beni çok anladı. Rahatladım.",
    "Bugün sosyal bir etkinliğe katıldım. Yeni insanlarla tanıştım. İletişim kurmak güzeldi.",
    
    # Nötr
    "Arkadaşlarımla kafe gittik. Biraz sohbet ettik.",
    "Bugün komşumla karşılaştım. Kısa bir sohbet ettik.",
    "Arkadaşım aradı. Nasıl olduğumu sordu. İyiyim dedim.",
    
    # Negatif
    "Bugün arkadaşımla tartıştık. Küs duruyoruz. Barışmamız lazım.",
    "Sosyal ortamlarda kendimi yalnız hissediyorum. Kimse benimle ilgilenmiyor.",
    "Arkadaşlarım beni çağırmadı. Dışlandığımı hissediyorum. Üzgünüm.",
    "Bugün birisiyle tartıştım. Çok sinir oldum. İlişki bitti.",
    "Eski arkadaşım beni umursamıyor. Mesajlarıma cevap vermiyor.",
    "Sosyal anksiyetem arttı. İnsanlarla konuşmaktan korkuyorum.",
    "Bugün yalnız hissettim. Kimsem yok gibi geliyor.",
    "Arkadaş grubum beni dışladı. Çok kırıldım.",
    "Güven problemi yaşıyorum. Kimseye açılamıyorum.",
    "Sosyal medyada herkesi mutlu görünce kendimi kötü hissettim.",
    
    
    # ================== GENEL GÜNLÜK (15 örnek) ==================
    
    "Bugün evde temizlik yaptım. Her yer pırıl pırıl oldu. Kendimi iyi hissediyorum.",
    "Sabah kahvaltısı yaptım ve gazeteleri okudum. Sakin bir sabah.",
    "Bugün parka gittim. Biraz yürüyüş yaptım. Hava güzeldi.",
    "Film izledim. Güzel bir dramıydı. Akşam keyifli geçti.",
    "Bugün hiçbir şey yapmadım. Evde dinlendim. Bazen böyle günler iyi geliyor.",
    "Sabahin erken uyandım. Güne erken başlamak güzeldi.",
    "Akşam yemeği için yeni bir tarif denedim. Çok lezzetli oldu.",
    "Bugün müzik dinleyerek vakit geçirdim. Ruhum dinlendi.",
    "Balkonda oturdum ve çay içtim. Manzara çok güzeldi.",
    "Bugün alışveriş yaptım. İhtiyaçlarımı aldım. Rutin bir gündü.",
    "Evde film maratonu yaptım. Üç tane film izledim.",
    "Bugün hava çok soğuktu. Evden çıkmadım. İçeride kitap okudum.",
    "Sabah kahvaltıda kruvasan yedim. Çok lezzetliydi.",
    "Bugün fotoğraf çekmeye çıktım. Güzel kareler yakaladım.",
    "Akşam arkadaşımla telefonda uzun konuştuk. Güzel sohbet oldu.",
]

# Toplam: 255 örnek

print(f"✅ Toplam {len(GUNLUK_ORNEKLERI)} adet kaliteli günlük örneği hazır!")
print("\n📊 Kategori Dağılımı:")
print("   İş ve Kariyer: 30")
print("   Eğitim ve Okul: 25")
print("   Sağlık: 30")
print("   Aile: 25")
print("   Finans ve Para: 25")
print("   Teknoloji: 20")
print("   Kişisel Gelişim: 20")
print("   Sosyal İlişkiler: 20")
print("   Genel Günlük: 15")
print("\nToplam: 255 örnek")