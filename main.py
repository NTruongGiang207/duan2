import discord
from discord.ext import commands
import json
import os
import random

TOKEN = "MTQwNDg3ODAzOTgzMzI1MTk0Nw.G-04aV.mWSCsuU4IIh3JzjSTThexKxiyeXorsP0BcU20Q"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=None, intents=intents)

DATA_FILE = "data/users.json"

# ======================
# DATA FUNCTIONS
# ======================

def update_user(user_id: int, new_data: dict):
    data = load_data()
    data[str(user_id)] = new_data
    save_data(data)


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)  # 👈 TẠO data/
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_user(user_id: int):
    data = load_data()
    uid = str(user_id)

    if uid not in data:
        data[uid] = {
            "money": 1000,
            "user_bank": 0,
            "location": "song",
            "rod": {
                "name": "Cần Gỗ",
                "durability": 100,
                "max": 100
            },
            "bait": {
                "giun": 10,
                "tom": 5,
                "moi_gia": 1
            },
            "inventory": {}
        }
        save_data(data)

    return data[uid]


def roll_fish_by_map(map_key):
    fishes = MAPS[map_key]["fish"]
    pool = []
    for name, info in fishes.items():
        pool.extend([name] * info["chance"])
    return random.choice(pool)



FISHES = {
    "Cá Chép": {"rarity": "Thường", "price": (50, 100), "chance": 60},
    "Cá Trê": {"rarity": "Thường", "price": (80, 120), "chance": 50},
    "Cá Hồi": {"rarity": "Hiếm", "price": (150, 250), "chance": 25},
    "Cá Mập": {"rarity": "Hiếm", "price": (300, 500), "chance": 10},
    "Rồng Biển": {"rarity": "Huyền Thoại", "price": (800, 1200), "chance": 3}
}

SHOP_ITEMS = {
    1: {
        "name": "Cần Sắt",
        "type": "rod",
        "price": 3000,
        "durability": 200
    },
    2: {
        "name": "Cần Vàng",
        "type": "rod",
        "price": 8000,
        "durability": 400
    },
    3: {
        "name": "Mồi Giun",
        "type": "bait",
        "price": 100,
        "amount": 5
    },
    4: {
        "name": "Mồi Tôm",
        "type": "bait",
        "price": 250,
        "amount": 5
    }
}



MAPS = {
    "song": {
        "name": "🌊 Sông",
        "fish": {
            "Cá Chép": {"rarity": "Thường", "price": (50,100), "chance": 60},
            "Cá Trê": {"rarity": "Thường", "price": (80,120), "chance": 50},
            "Cá Sấu": {"rarity": "Hiếm", "price": (300,500), "chance": 10}
        }
    },
    "bien": {
        "name": "🌊 Biển",
        "fish": {
            "Cá Hồi": {"rarity": "Hiếm", "price": (150,250), "chance": 30},
            "Cá Mập": {"rarity": "Hiếm", "price": (300,500), "chance": 15},
            "Rồng Biển": {"rarity": "Huyền Thoại", "price": (800,1200), "chance": 3}
        }
    },
    "hang": {
        "name": "🕳️ Hang",
        "fish": {
            "Cá Bóng Ma": {"rarity": "Hiếm", "price": (400,600), "chance": 20},
            "Cá Cổ Đại": {"rarity": "Huyền Thoại", "price": (1200,1800), "chance": 2}
        }
    }
}

WEATHER = {
    "nang": {"name": "☀️ Nắng", "bonus": 1.0},
    "mua": {"name": "🌧️ Mưa", "bonus": 1.3},
    "bao": {"name": "⛈️ Bão", "bonus": 1.6}
}

def current_weather():
    return random.choice(list(WEATHER.values()))



def get_fish_price(fish_name):
    if fish_name in FISHES:
        return FISHES[fish_name]["price"]
    for m in MAPS.values():
        if fish_name in m["fish"]:
            return m["fish"][fish_name]["price"]
    return (0, 0)

# ======================
# BOT READY
# ======================
@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"✅ Bot online: {bot.user}")
    print(f"🔁 Slash synced: {len(synced)}")

# ======================
# /profile
# ======================
@bot.tree.command(name="profile", description="Xem thông tin người chơi")
async def profile(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    avatar = interaction.user.display_avatar.url


    embed = discord.Embed(
        title="👤 HỒ SƠ NGƯỜI CHƠI",
        color=0x3498db
    )
    embed.set_thumbnail(url=avatar)

    embed.add_field(
        name="💰 Tiền",
        value=f"{user['money']} 🪙",
        inline=False
    )

    embed.add_field(
        name="🎣 Cần câu",
        value=f"{user['rod']['name']} ({user['rod']['durability']}/{user['rod']['max']})",
        inline=False
    )

    embed.add_field(
        name="🪱 Mồi",
        value=(
            f"Giun: {user['bait']['giun']}\n"
            f"Tôm: {user['bait']['tom']}\n"
            f"Mồi giả: {user['bait']['moi_gia']}"
        ),
        inline=False
    )

    embed.add_field(
        name="📍 Khu vực",
        value=user["location"],
        inline=False
    )

    await interaction.response.send_message(embed=embed)


# ======================
# /cau
# ======================
@bot.tree.command(name="cau", description="Câu cá kiếm cá và tiền")
async def cau(interaction: discord.Interaction):
    user = get_user(interaction.user.id)

    if user["rod"]["durability"] <= 0:
        await interaction.response.send_message(
            "❌ Cần câu đã hỏng! Hãy mua cần mới.",
            ephemeral=True
        )
        return

    map_key = user.get("location", "song")
    if map_key not in MAPS:
        map_key = "song"
        user["location"] = "song"

    weather = current_weather()

    fish_name = roll_fish_by_map(map_key)
    fish_info = MAPS[map_key]["fish"][fish_name]

    base_money = random.randint(*fish_info["price"])
    earned = int(base_money * weather["bonus"])

    durability_loss = random.randint(5, 15)

    # cập nhật data
    user["rod"]["durability"] = max(0, user["rod"]["durability"] - durability_loss)

    inv = user.get("inventory", {})
    inv[fish_name] = inv.get(fish_name, 0) + 1
    user["inventory"] = inv

    update_user(interaction.user.id, user)
    

    embed = discord.Embed(title="🎣 BẠN ĐÃ CÂU ĐƯỢC CÁ!", color=0x1abc9c)
    embed.set_author(
        name=interaction.user.display_name,
        icon_url=interaction.user.display_avatar.url
    )

    embed.add_field(name="📍 Khu vực", value=MAPS[map_key]["name"], inline=True)
    embed.add_field(name="⛅ Thời tiết", value=weather["name"], inline=True)

    embed.add_field(
        name="🐟 Cá",
        value=f"{fish_name} ({fish_info['rarity']})",
        inline=False
    )

    embed.add_field(
    name="💰 Giá trị ước tính",
    value=f"{earned} 🪙",
    inline=False
    )


    embed.add_field(
        name="🔧 Độ bền cần",
        value=f"-{durability_loss} ({user['rod']['durability']}/{user['rod']['max']})",
        inline=False
    )

    await interaction.response.send_message(embed=embed)



# ======================
# /inventory
# ======================

@bot.tree.command(name="inventory", description="Xem túi cá của bạn")
async def inventory(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    inv = user.get("inventory", {})

    embed = discord.Embed(
        title="🎒 TÚI ĐỒ",
        color=0xf1c40f
    )

    if not inv:
        embed.description = "❌ Túi đồ trống."
    else:
        for fish, amount in inv.items():
            rarity = FISHES.get(fish, {"rarity": "Không rõ"})["rarity"]
            embed.add_field(
                name=f"🐟 {fish}",
                value=f"Số lượng: {amount}\nĐộ hiếm: {rarity}",
                inline=False
            )

    await interaction.response.send_message(embed=embed)

# ======================
# /sell
# ======================
@bot.tree.command(name="sell", description="Bán cá trong túi")
async def sell(
    interaction: discord.Interaction,
    fish_name: str,
    amount: int
):
    user = get_user(interaction.user.id)
    inv = user.get("inventory", {})

    if fish_name not in inv:
        await interaction.response.send_message("❌ Bạn không có loại cá này.", ephemeral=True)
        return

    if amount <= 0 or inv[fish_name] < amount:
        await interaction.response.send_message("❌ Số lượng không hợp lệ.", ephemeral=True)
        return

    fish_price = random.randint(*get_fish_price(fish_name))
    total = fish_price * amount


    inv[fish_name] -= amount
    if inv[fish_name] <= 0:
        del inv[fish_name]

    user["money"] += total
    user["inventory"] = inv

    update_user(interaction.user.id, user)

    await interaction.response.send_message(
        f"💰 Đã bán **{amount} {fish_name}** và nhận **{total} 🪙**"
    )

# ======================
# /sellall
# ======================

@bot.tree.command(name="sellall", description="Bán toàn bộ cá")
async def sellall(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    inv = user.get("inventory", {})

    if not inv:
        await interaction.response.send_message("❌ Túi cá trống.", ephemeral=True)
        return

    total = 0
    for fish, amount in inv.items():
        price = random.randint(*get_fish_price(fish))
        total += price * amount


    user["inventory"] = {}
    user["money"] += total

    update_user(interaction.user.id, user)

    await interaction.response.send_message(
        f"💰 Đã bán tất cả cá, nhận **{total} 🪙**"
    )

# ======================
# /shop
# ======================
@bot.tree.command(name="shop", description="Xem cửa hàng")
async def shop(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🏪 CỬA HÀNG",
        color=0xe67e22
    )

    for item_id, item in SHOP_ITEMS.items():
        if item["type"] == "rod":
            desc = f"Độ bền: {item['durability']}"
        else:
            desc = f"+{item['amount']} mồi"

        embed.add_field(
            name=f"{item_id}. {item['name']} - {item['price']} 🪙",
            value=desc,
            inline=False
        )

    embed.set_footer(text="Dùng /buy <id> để mua")
    await interaction.response.send_message(embed=embed)

# ======================
# /buy
# ======================
@bot.tree.command(name="buy", description="Mua đồ trong shop")
async def buy(interaction: discord.Interaction, item_id: int):
    user = get_user(interaction.user.id)

    if item_id not in SHOP_ITEMS:
        await interaction.response.send_message("❌ Vật phẩm không tồn tại.", ephemeral=True)
        return

    item = SHOP_ITEMS[item_id]

    if user["money"] < item["price"]:
        await interaction.response.send_message("❌ Không đủ tiền.", ephemeral=True)
        return

    user["money"] -= item["price"]

    if item["type"] == "rod":
        user["rod"] = {
            "name": item["name"],
            "durability": item["durability"],
            "max": item["durability"]
        }
    else:
        bait_name = "giun" if "Giun" in item["name"] else "tom"
        user["bait"][bait_name] += item["amount"]

    update_user(interaction.user.id, user)

    await interaction.response.send_message(
        f"✅ Đã mua **{item['name']}**!"
    )



@bot.tree.command(name="bank", description="Ngân hàng cá nhân")
async def bank(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    avatar = interaction.user.display_avatar.url


    embed = discord.Embed(
        title="🏦 NGÂN HÀNG",
        color=0x9b59b6
    )


    embed.set_thumbnail(url=avatar)


    embed.add_field(name="💰 Ví", value=f"{user['money']:,} 🪙", inline=False)
    embed.add_field(name="🏦 Bank", value=f"{user['user_bank']:,} 🪙", inline=False)

    await interaction.response.send_message(
        embed=embed,
        view=BankView(interaction.user.id),
        ephemeral=True
    )


# ---------- BANK BUTTON + MODAL ----------

class DepositModal(discord.ui.Modal, title="💰 Gửi tiền"):
    amount = discord.ui.TextInput(label="Số tiền gửi", placeholder="VD: 5000")

    async def on_submit(self, interaction: discord.Interaction):
        user = get_user(interaction.user.id)

        if not self.amount.value.isdigit():
            return await interaction.response.send_message("❌ Vui lòng nhập số.", ephemeral=True)

        amt = int(self.amount.value)

        if amt <= 0 or user["money"] < amt:
            return await interaction.response.send_message("❌ Không đủ tiền.", ephemeral=True)

        user["money"] -= amt
        user["user_bank"] += amt
        update_user(interaction.user.id, user)

        await interaction.response.send_message(f"✅ Đã gửi **{amt:,} 🪙** vào ngân hàng.", ephemeral=True)

class WithdrawModal(discord.ui.Modal, title="🏧 Rút tiền"):
    amount = discord.ui.TextInput(label="Số tiền rút", placeholder="VD: 3000")

    async def on_submit(self, interaction: discord.Interaction):
        user = get_user(interaction.user.id)

        if not self.amount.value.isdigit():
            return await interaction.response.send_message("❌ Vui lòng nhập số.", ephemeral=True)

        amt = int(self.amount.value)

        if amt <= 0 or user["user_bank"] < amt:
            return await interaction.response.send_message("❌ Bank không đủ tiền.", ephemeral=True)

        user["user_bank"] -= amt
        user["money"] += amt
        update_user(interaction.user.id, user)

        await interaction.response.send_message(f"🏧 Đã rút **{amt:,} 🪙**", ephemeral=True)

class BankView(discord.ui.View):
    def __init__(self, uid: int):
        super().__init__(timeout=60)
        self.uid = uid

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.uid

    @discord.ui.button(label="Gửi tiền", style=discord.ButtonStyle.green, emoji="💰")
    async def deposit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DepositModal())

    @discord.ui.button(label="Rút tiền", style=discord.ButtonStyle.blurple, emoji="🏧")
    async def withdraw(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WithdrawModal())




@bot.tree.command(name="menu", description="Menu nhanh")
async def menu(interaction: discord.Interaction):
    avatar = interaction.user.display_avatar.url
    view = QuickView(interaction.user.id)
    embed = discord.Embed(
        title="🎮 MENU NHANH",
        description="Câu cá và bán cá nhanh",
        color=0x5865F2
    )
    embed.set_thumbnail(url=avatar)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


from discord.ui import View, Button

class QuickView(View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.user_id

    @discord.ui.button(label="🎣 Câu nhanh", style=discord.ButtonStyle.green)
    async def quick_fish(self, interaction: discord.Interaction, button: Button):
        await cau(interaction)

    @discord.ui.button(label="💰 Bán tất cả", style=discord.ButtonStyle.blurple)
    async def quick_sell(self, interaction: discord.Interaction, button: Button):
        await sellall(interaction)


@bot.tree.command(name="map", description="Đổi khu vực câu")
async def change_map(interaction: discord.Interaction, map_key: str):
    user = get_user(interaction.user.id)

    if map_key not in MAPS:
        await interaction.response.send_message("❌ Map không tồn tại.", ephemeral=True)
        return

    user["location"] = map_key
    update_user(interaction.user.id, user)

    await interaction.response.send_message(
        f"✅ Đã chuyển sang {MAPS[map_key]['name']}", ephemeral=True
    )

@bot.tree.command(name="leaderboard", description="Bảng xếp hạng tiền")
async def leaderboard(interaction: discord.Interaction):
    data = load_data()
    sorted_users = sorted(
        data.items(),
        key=lambda x: x[1].get("money", 0),
        reverse=True
    )[:10]

    embed = discord.Embed(title="🏆 TOP GIÀU CÓ", color=0xf1c40f)

    for i, (uid, info) in enumerate(sorted_users, start=1):
        embed.add_field(
            name=f"#{i}",
            value=f"<@{uid}> – {info.get('money',0)} 🪙",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
