import lz4.block
import msgpack
import json
import os
import tkinter as tk
from tkinter import filedialog
# Extension hook function
root = tk.Tk()
root.withdraw()  # Hide the main window
def ext_hook(code, data):
    if code == 99:
        decompressed_size = msgpack.unpackb(data[:5])
        return msgpack.unpackb(lz4.block.decompress(data[5:], uncompressed_size=decompressed_size))
    else:
        return msgpack.ExtType(code, data)


all_objects = []
file_names = ["BGM.json", "Battle.json", "Buff.json", "Card.json", "CardAbility.json", "CardBookTab.json", "CardLevel.json", "CharaBook.json", "CharaBookAction.json", "Character.json", "Charm.json", "CharmAbility.json", "CharmAbilityPack.json", "CharmAbilityTypeReaction.json", "CharmInitialize.json", "Commission.json", "CommissionReward.json", "Costume.json", "CostumeSet.json", "Deck.json", "Dialog.json", "DialogButton.json", "DifficultyInfo.json", "Divination.json", "DungeonEvent.json", "Effect.json", "Enemy.json", "EnemyAction.json", "EnemyActionPattern.json", "EnemyGroup.json", "EnemySpawn.json", "Glossary.json", "HomeTimelineConfig.json", "Map.json", "MapBoss.json", "Mission.json", "MissionLevel.json", "MissionLottery.json", "MissionNode.json", "MissionNodeLimit.json", "Reaction.json", "Rest.json", "Reward.json", "Setting.json", "Shop.json", "ShopChara.json", "ShopProduct.json", "ShopRack.json", "SpecialCard.json", "SpecialCardGroup.json", "Story.json", "Style.json", "StyleAbility.json", "StyleLevel.json", "Treasure.json", "Tutorial.json", "TutorialPage.json", "Vibration.json", "Voice.json"]

path_masterdata = filedialog.askopenfilename(title="Locate Masterdata File")
path_exported_masterdata = os.path.splitext(path_masterdata.split("/")[-1])[0] + "_unpacked"
if path_masterdata:
    print(f"Selected File: {path_masterdata}")
else:
    print("No file selected")
    sys.exit(1)
    
with open(path_masterdata, "rb") as file:
    data = msgpack.Unpacker(file, ext_hook=ext_hook, raw=False)
    for obj in data:
        obj_json = json.dumps(obj)
        all_objects.append(json.loads(obj_json))

if len(all_objects) > 0:
    all_objects = all_objects[1:]

os.makedirs(path_exported_masterdata, exist_ok=True)

# Iterate over each object and write it to a separate file
for obj, file_name in zip(all_objects, file_names):
    # Write the object to the corresponding file
    file_path = os.path.join(path_exported_masterdata, file_name)
    with open(file_path, "w") as json_file:
        json.dump(obj, json_file)

print(f"Data written")