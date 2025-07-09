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
        self.power = random.randint(30, 60)  # Pokémon'un gücünü rastgele bir değer olarak ayarlar
        self.hp = random.randint(200, 400)  # Pokémon'un can puanını rastgele bir değer olarak ayarlar
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
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}' # İstek için URL API
        async with aiohttp.ClientSession() as session:  # HTTP oturumu açma
            async with session.get(url) as response: # GET isteği gönderme
                if response.status == 200:
                    data = await response.json() # JSON yanıtının alınması ve çözümlenmesi
                    return data['height'] # Pokémon'un yüksekliğini döndürür
                else: 
                    return random.randint(1, 20)  # İstek başarısız olursa rastgele bir yükseklik döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
            self.height = await self.get_height() # Henüz yüklenmemişse bir yüksekliğin geri alınması
        return f"""Pokémonunuzun İsmi: {self.name}
        Canı: {self.hp}
        Güç: {self.power}
        Yüksekliği: {self.height}""" # Pokémon hakkında bilgi döndürür

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
                
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullandı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu şimdi {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"
    
                

                
class Wizard(Pokemon):
    pass
    
class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"
