# MapUtil

Datapack & resourcepack providing utilities for mapmaking.  
Minecraft version: 1.21.5

# Mcdoc

Mcdoc is a feature of VSCode [Spyglass extension](https://marketplace.visualstudio.com/items?itemName=SPGoding.datapack-language-server).  
If you're using the extension, you can copy `mcdoc/` folder to the root of your workspace.  
It provides syntax highlighting and autocompletion of custom data provided by this pack.

# Datapack

## Block Tags

- `#mu:no_hitbox`
  - All blocks which don't block projectile motion.
  - Includes blocks which slows some entities down (e.g. cobweb).

## Entity Tags

- `#mu:monster`
  - All monsters.
  - `rabbit` is not included, so killer bunny may require extra tests.
- `#mu:non_living`
  - Non living entities.
  - It's a bit different from the gamecode `LivingEntity` definition - `armor_stand` is included in this tag.

## Mob Effect Tags

- `#mu:beneficial`
  - All beneficial effects.
- `#mu:neutral`
  - All neutral effects.
- `#mu:harmful`
  - All harmful effects.
- `#mu:instantaneous`
  - All instantaneous effects.
- `#mu:status`
  - All non-instantaneous effects.

## Predicates

- `mu:is_baby`
  - Context: Entity
  - Passes if the entity is baby.
- `mu:is_flying`
  - Context: Entity
  - Passes if the entity is flying.
- `mu:is_on_fire`
  - Context: Entity
  - Passes if the entity is on fire.
- `mu:is_on_ground`
  - Context: Entity
  - Passes if the entity is on ground.
- `mu:is_sneaking`
  - Context: Entity
  - Passes if the entity is sneaking.
- `mu:is_sprinting`
  - Context: Entity
  - Passes if the entity is sprinting.
- `mu:is_swimming`
  - Context: Entity
  - Passes if the entity is swimming.
- `mu:has_passenger`
  - Context: Entity
  - Passes if the entity has passenger.
- `mu:has_vehicle`
  - Context: Entity
  - Passes if the entity has vehicle.
- `mu:is_in_water`
  - Context: Entity
  - Passes if the entity is in water (checks for feet location).
- `mu:rabbit/is_evil`
  - Context: Entity
  - Passes if the entity is killer bunny.
- `mu:player/can_crit`
  - Context: Entity (player)
  - Passes if the player may be able to perform crit attack.
  - Some conditions are not checked in this predicate:
    1. Player's attack cooldown must be >90%
    2. The victim must be `LivingEntity`
- `mu:location/is_water`
  - Context: Location
  - Passes if the location is in water.

## Item Modifiers

- `mu:grow`
  - Item count +1.
- `mu:shrink`
  - Item count -1.

## Function Macro

### `mu:callback_macro`

```mcfunction
$function $(function)
```

## Interaction System

Triggers functions when an interaction is clicked.

- The functions are recorded in custom data of the interaction.
  - `mu.on_interact`: Right click reaction
  - `mu.on_attack`: Left click reaction

### Data Structure

- (optional) string `as_player`: The function to be run as the player clicked the interaction, at the interaction.
- (optional) string `as_this`: The function to be run as & at the interaction.

### Example

```mcfunction
summon interaction ~ ~ ~ { \
  data: { \
    mu: { \
      on_interact: {as_player: "foo:bar"} \
    } \
  } \
}
```

## Text Refresh System

Refreshes translatable texts on text display entities and signs.  
Texts are refreshed once per second.

### Text Display

- The text display should have `mu.translated` tag.

#### Example

```mcfunction
summon text_display ~ ~ ~ { \
  text: {translate: "block.minecraft.stone"}, \
  Tags: ["mu.translated"], \
}
```

### Sign

- Summon a marker with `mu.translated` tag at the location of the sign.
- The sign should have `mu.translated` custom data.
  - Data value: Empty object `{}`.
- The marker is automatically removed when the sign disappears.

#### Example

```mcfunction
summon marker ~ ~ ~ {Tags: ["mu.translated"]}
data modify block ~ ~ ~ components.minecraft:custom_data.mu.translated set value {}
```

## Player Data Storage System

Stores per-player data in data storage.

### Load data

Always run function `mu:load_player_data` as the player before use.

### Data structure

Data storage ID: `mu:player_data`

- compound `root`: Stores arbitrary data.
  - compound `mu`: Data provided by MapUtil.
    - int\[4\] `uuid`: UUID of the player. Do NOT modify this field.

### Example

```mcfunction
# As a player
function mu:load_player_data
data modify storage mu:player_data root.foo set value "bar"
```

### Mcdoc Support

> [!Note]
> [Here](https://spyglassmc.com/user/mcdoc/) is mcdoc syntax documentation.

The dispatcher of player data storage is `mu:player_data`.

#### Example

```
// Specifies data type of root.foo
dispatch mu:player_data[foo] to struct Foo {
  bar?: string
}
```

## Shared Actionbar

WIP

## Events

Function with specific tags will be invoked by some events.

### `#mu:tick`

- The tick function.
- To make sure the commands run in correct order, if the tick function interacts with MapUtil, it's recommended to hook the function on this tag instead of `#minecraft:tick`.
- To be more specific, the affected systems include:
  - Shared Actionbar (WIP)

### `#mu:player_event/on_first_join`

- Runs when a player first joins the world.
- As & at the player.

### `#mu:player_event/on_login`

- Runs when a player joins the world.
- As & at the player.

### `mu:player_event/on_die`

- Runs when a player dies.
- As & at the death location of the player.
- Subtick timing - this function tag runs:
  - After death drop (if `keepInventory` = `false`).
  - Before respawn (even if `doImmediateRespawn` = `true`).

### `#mu:player_event/on_respawn`

- Runs when a player respawns.
- As & at the player.

### `#mu:entity_event/on_aec_spawned`

- Runs when an area effect cloud appears.
- As & at the new AEC.
- The `potion_contents.custom_effects` of the AEC is copied to `custom_effects` of data storage `mu:aec`.
- It's recommended to identify AECs in this function tag to avoid redundant entity NBT serialization.
  - Checking data storage is way faster than checking entity NBT.
  - You can give AECs tags in this function tag.

> [!Tip]
> Currently, AEC spawned by lingering potion inherits `custom_data` component.  
> Also, vanilla potion effects can be tested with `potion_contents` component predicate.  
> Only creeper explosion detection still requires custom effect NBT test.

# Resourcepack

> [!Note]
> The datapack can run without the resourcepack.

## Fonts

### `minecraft:seven`

- The classic Mojangles font, regardless of Force Unicode settings.

### `mu:neg/*`

- Negative width version of fonts.
- Including:
  - `neg/default`
  - `neg/seven`
  - `neg/uniform`
  - `neg/alt`
  - `neg/illageralt`

### `mu:half_neg/*`

- Half negative width version of fonts.
- Including:
  - `half_neg/default`
  - `half_neg/seven`
  - `half_neg/uniform`
  - `half_neg/alt`
  - `half_neg/illageralt`

> [!Note]
> Because the full negative uniform font takes *long* time to load, by default it's configured to only include some characters:
>
> - Characters with Mojangles counterpart
> - Keyboard key names (e.g. "Left Shift") in all languages
>
> This behavior is configurable in `generate_fonts.py`.  
> To change this, you can:
>
> 1. modify `unifont_charset` to include other characters, or
> 1. modify the behavior of function `build_charset()`, which has access to vanilla translations, or
> 1. set `INCLUDE_ALL_CODEPOINTS` to `True` (not recommended - 227k entries is too heavy for the game).
>
> Example:
> ```python
> unifont_charset = set(range(256)) | set(ord(c) for s in ["なんだそりゃ", "＞＜"] for c in s)
> ```
>
> Example:
> ```python
> def build_charset(repo_archive: ZipFile, /):
>   # ...
>   # Trivia: some languages don't use Roman numerals to represent enchantment levels
>   key_patterns = [re.compile(r"key\.keyboard\..+"), re.compile(r"enchantment\.level\.\d+")]
>   # ...
> ```

### `mu:space`

Provides fixed width spaces.

- `\u**0N` (`N` = 0 ~ b): Controls integer width
  - Width = `2^N`
- `\u**1N` (`N` = 0 ~ 6): Controls fractional width
  - Width = `2^(-N)`
- `\u*N**` (`N` = 0 ~ 1): Controls the sign of width
  - `N` = 0: Positive width
  - `N` = 1: Negative width
- `\uN***` (`N` = e ~ f): Controls category
  - `N` = e: Visible in all settings
  - `N` = f: Only visible when Force Unicode is ON
- Example: The string `\ue102\uf001`
  - Width = -4 when Force Unicode is OFF (`\ue102`: -4, `\uf001`: 0)
  - Width = -2 when Force Unicode is ON (`\ue102`: -4, `\uf001`: 2)

## Shaders

The constants and functions are defined in `mu:util.glsl`.

### `PI` & `TAU`

- `PI` represents the mathematical constant π, the ratio of a circle's circumference to its diameter.
- `TAU` is twice the value of `PI`.

### `roughlyEqual`

```glsl
bool roughlyEqual(float a, float b)
```

- Returns `true` if the difference between the two inputs are less than 1e-4.

### `isGui`

```glsl
bool isGui(mat4 ProjMat)
```

- Returns `true` if the element is a part of GUI.

### `getGuiScale`

```glsl
float getGuiScale(mat4 ProjMat, vec2 ScreenSize)
```

- Returns the GUI scale value.

## Armor Trims

- Provides empty trim textures on `wings` layer.
  - This prevents elytra from displaying the "missing" texture when trimmed.

# Changelog

Only breaking changes are listed.

## v1.2.0 (upcoming)

- Rename the namespace `maputil:` to `mu:`.
  - Tag prefixes are also affected (`maputil.` → `mu.`).
- Rename the predicate `maputil:is_killer_bunny` to `mu:rabbit/is_evil`
