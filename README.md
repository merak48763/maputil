# MapUtil

Utility datapack & resourcepack providing utilities for mapmaking.  
Minecraft version: The upcoming game drop (supposed to be 1.21.5)

# Mcdoc

Mcdoc is a feature of VSCode [Spyglass extension](https://github.com/SpyglassMC/Spyglass).  
If you're using the extension, you can copy `mcdoc/` folder to the root of your workspace.  
It provides syntax highlighting and autocompletion of custom data provided by this pack.

# Datapack

## Block Tags

- `#maputil:no_hitbox`
  - All blocks which don't block projectile motion.
  - Includes blocks which slows some entities down (e.g. cobweb).

## Entity Tags

- `#maputil:monster`
  - All monsters.
  - `rabbit` is not included, so killer bunny may require extra tests.
- `#maputil:non_living`
  - Non living entities.
  - It's a bit different from the gamecode `LivingEntity` definition - `armor_stand` is included in this tag.

## Mob Effect Tags

- `#maputil:beneficial`
  - All beneficial effects.
- `#maputil:neutral`
  - All neutral effects.
- `#maputil:harmful`
  - All harmful effects.
- `#maputil:instantaneous`
  - All instantaneous effects.
- `#maputil:status`
  - All non-instantaneous effects.

## Predicates

- `maputil:has_passenger`
  - Context: Entity
  - Passes if the entity has passenger.
- `maputil:has_vehicle`
  - Context: Entity
  - Passes if the entity has vehicle.
- `maputil:is_killer_bunny`
  - Context: Entity
  - Passes if the entity is killer bunny

## Item Modifiers

- `maputil:grow`
  - Item count +1.
- `maputil:shrink`
  - Item count -1.

## Function Macro

### `maputil:callback_macro`

```mcfunction
$function $(function)
```

## Interaction System

Triggers functions when an interaction is clicked.

- The functions are recorded in custom data of the interaction.
  - `maputil.on_interact`: Right click reaction
  - `maputil.on_attack`: Left click reaction

### Data Structure

- (optional) string `as_player`: The function to be run as the player clicked the interaction, at the interaction.
- (optional) string `as_this`: The function to be run as & at the interaction.

### Example

```mcfunction
summon interaction ~ ~ ~ { \
  data: { \
    maputil: { \
      on_interact: {as_player: "foo:bar"} \
    } \
  } \
}
```

## Text Refresh System

Refreshes translatable texts on text display entities and signs.  
Texts are refreshed once per second.

### Text Display

- The text display should have `maputil.translated` tag.

#### Example

```mcfunction
summon text_display ~ ~ ~ { \
  text: {translate: "block.minecraft.stone"}, \
  Tags: ["maputil.translated"], \
}
```

### Sign

- Summon a marker with `maputil.translated` tag at the location of the sign.
- The sign should have `maputil.translated` custom data.
  - Data value: Empty object `{}`.
- The marker is automatically removed when the sign disappears.

#### Example

```mcfunction
summon marker ~ ~ ~ {Tags: ["maputil.translated"]}
data modify block ~ ~ ~ components.minecraft:custom_data.maputil.translated set value {}
```

## Player Data Storage System

Stores per-player data in data storage.

### Load data

Always run function `maputil:load_player_data` as the player before use.

### Data structure

Data storage ID: `maputil:player_data`

- compound `root`: Stores arbitrary data.
  - compound `maputil`: Data provided by MapUtil.
    - int\[4\] `uuid`: UUID of the player. Do NOT modify this field.

### Example

```mcfunction
# As a player
function maputil:load_player_data
data modify storage maputil:player_data root.foo set value "bar"
```

### Mcdoc Support

> [!Note]
> [Here](https://spyglassmc.com/user/mcdoc/) is mcdoc syntax documentation.

The dispatcher of player data storage is `maputil:player_data`.

#### Example

```
// Specifies data type of root.foo
dispatch maputil:player_data[foo] to struct Foo {
  bar?: string
}
```

## Events

Function with specific tags will be invoked by some events.

### `#maputil:tick`

- The tick function.
- To make sure the commands run in correct order, if the tick function interacts with MapUtil, it's recommended to hook the function on this tag instead of `#minecraft:tick`.
- To be more specific, affected systems include:
  - Player Data Storage

### `#maputil:player_event/on_first_join`

- Runs when a player first joins the world.
- As & at the player.

### `#maputil:player_event/on_login`

- Runs when a player joins the world.
- As & at the player.

### `#maputil:player_event/on_respawn`

- Runs when a player respawns.
- As & at the player.

### `#maputil:entity_event/on_aec_spawned`

- Runs when an area effect cloud appears.
- As & at the new AEC.
- The `potion_contents.custom_effects` of the AEC is copied to `custom_effects` of data storage `maputil:aec`.
- It's recommended to identify AECs in this function tag to avoid redundant entity NBT checks.
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

### `maputil:neg/*`

- Negative width version of fonts.
- Including:
  - `neg/default`
  - `neg/seven`
  - `neg/uniform`
  - `neg/alt`
  - `neg/illageralt`

### `maputil:half_neg/*`

- Half negative width version of fonts.
- Including:
  - `half_neg/default`
  - `half_neg/seven`
  - `half_neg/uniform`
  - `half_neg/alt`
  - `half_neg/illageralt`

### `maputil:space`

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

The functions are in `maputil:util.glsl`.

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
int getGuiScale(mat4 ProjMat, vec2 ScreenSize)
```

- Returns the GUI scale value.
