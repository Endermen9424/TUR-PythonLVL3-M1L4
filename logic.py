import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.height = None
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür
                
    async def get_height(self):
        # PokeAPI aracılığıyla bir pokémonun yüksekliğini almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:  # HTTP oturumu açma
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['height']
                else:
                    return random.randint(1, 20)  # İstek başarısız olursa rastgele bir yükseklik döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
            self.height = await self.get_height()
        return f"Pokémonunuzun ismi: {self.name} yüksekliği: {self.height}"  # Pokémon adını içeren dizeyi döndürür

    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    img_url = data['sprites']["front_default"]  # Pokémon'un görüntü URL'sini alma
                    return img_url  # Pokémon görüntüsünün URL'sini döndürür
                else:
                    return None
