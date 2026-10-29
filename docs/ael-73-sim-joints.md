# AEL-73: суставные лимиты в USD Isaac G1

Слои ассета Isaac 6.2 прочитаны через `pxr.Sdf` 2026-10-29. Это значения **симуляции**, а не подтверждённые параметры реального робота. Лимиты `PhysicsRevoluteJoint` указаны в градусах; `maxForce` — исходное значение атрибута `drive:angular:physics:maxForce`.

| Слой | SHA-256 |
| --- | --- |
| [g1_29dof_with_hand_rev_1_0_physics.usd](https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/6.2/Isaac/Robots/Unitree/G1/configuration/g1_29dof_with_hand_rev_1_0_physics.usd) | `a5dd8e61a634043a65e90251eec4a3c7f25d84a999fa02a3bf3ec6fd67d4df67` |
| [three_finger_hand/three_finger_hand_physics_left.usd](https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/6.2/Isaac/Robots/Unitree/G1/configuration/three_finger_hand/three_finger_hand_physics_left.usd) | `ee231ebe0300341fa87b83a3e685654a0832eeb4041d0a70ce66b34a2e78893b` |
| [three_finger_hand/three_finger_hand_physics_right.usd](https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/6.2/Isaac/Robots/Unitree/G1/configuration/three_finger_hand/three_finger_hand_physics_right.usd) | `d0625204ac01a876d7e89388f87181b341b2af75dc1cccd21d87ba629c57e535` |

Все 43 имени совпали с суставами, прописанными в локальном `isaac_sc/Unitree_base_bot.usd`: 29 суставов тела и по 7 в каждой кисти.

Для сравнения взят [официальный URDF Unitree `g1_29dof_with_hand_rev_1_0.urdf`](https://github.com/unitreerobotics/unitree_ros/blob/deeb607f3a8945a394f53068c28b3a88dde7ff06/robots/g1_description/g1_29dof_with_hand_rev_1_0.urdf), SHA-256 `97da67732d067c3147fc5fb7b7bafc8982718f4e7f8c92ff82266a4d9c07200d`. В нём также 43 подвижных сустава с теми же именами. Численные `lower/upper` после перевода радиан → градусы совпадают с USD с точностью 0,2° для 41 сустава. Исключения:

| Сустав | USD, ° | URDF Unitree, ° | Разница |
| --- | --- | --- | --- |
| `left_hand_thumb_1_joint` | −41,5…60 | −35…60 | Нижняя граница USD ниже на 6,5°. |
| `right_hand_thumb_1_joint` | −60…41,5 | −60…35 | Верхняя граница USD выше на 6,5°. |

Числа `maxForce` в USD отличаются от `effort` в URDF для шести суставов: четыре голеностопа и `waist_roll_joint`/`waist_pitch_joint` имеют в USD `50`, в URDF `35`. Атрибуты относятся к разным описаниям привода; из численного различия не следует, что один из файлов ошибочен. Лимиты и допустимые усилия конкретного робота всё ещё нужно подтвердить по его конфигурации.

| Сустав | Нижний лимит, ° | Верхний лимит, ° | maxForce |
| --- | ---: | ---: | ---: |
| `left_hip_pitch_joint` | -145.00 | 165.00 | 88.00 |
| `right_hip_pitch_joint` | -145.00 | 165.00 | 88.00 |
| `waist_yaw_joint` | -150.00 | 150.00 | 88.00 |
| `left_hip_roll_joint` | -30.00 | 170.00 | 139.00 |
| `right_hip_roll_joint` | -170.00 | 30.00 | 139.00 |
| `waist_roll_joint` | -29.79 | 29.79 | 50.00 |
| `left_hip_yaw_joint` | -158.00 | 158.00 | 88.00 |
| `right_hip_yaw_joint` | -158.00 | 158.00 | 88.00 |
| `waist_pitch_joint` | -29.79 | 29.79 | 50.00 |
| `left_knee_joint` | -5.00 | 165.00 | 139.00 |
| `right_knee_joint` | -5.00 | 165.00 | 139.00 |
| `left_shoulder_pitch_joint` | -177.00 | 153.00 | 25.00 |
| `right_shoulder_pitch_joint` | -177.00 | 153.00 | 25.00 |
| `left_ankle_pitch_joint` | -50.00 | 30.00 | 50.00 |
| `right_ankle_pitch_joint` | -50.00 | 30.00 | 50.00 |
| `left_shoulder_roll_joint` | -91.00 | 129.00 | 25.00 |
| `right_shoulder_roll_joint` | -129.00 | 91.00 | 25.00 |
| `left_ankle_roll_joint` | -15.00 | 15.00 | 50.00 |
| `right_ankle_roll_joint` | -15.00 | 15.00 | 50.00 |
| `left_shoulder_yaw_joint` | -150.00 | 150.00 | 25.00 |
| `right_shoulder_yaw_joint` | -150.00 | 150.00 | 25.00 |
| `left_elbow_joint` | -60.00 | 120.00 | 25.00 |
| `right_elbow_joint` | -60.00 | 120.00 | 25.00 |
| `left_wrist_roll_joint` | -113.00 | 113.00 | 25.00 |
| `right_wrist_roll_joint` | -113.00 | 113.00 | 25.00 |
| `left_wrist_pitch_joint` | -92.50 | 92.50 | 5.00 |
| `right_wrist_pitch_joint` | -92.50 | 92.50 | 5.00 |
| `left_wrist_yaw_joint` | -92.50 | 92.50 | 5.00 |
| `right_wrist_yaw_joint` | -92.50 | 92.50 | 5.00 |
| `left_hand_index_0_joint` | -90.00 | 0.00 | 1.40 |
| `left_hand_middle_0_joint` | -90.00 | 0.00 | 1.40 |
| `left_hand_thumb_0_joint` | -60.00 | 60.00 | 2.45 |
| `left_hand_index_1_joint` | -100.00 | 0.00 | 1.40 |
| `left_hand_middle_1_joint` | -100.00 | 0.00 | 1.40 |
| `left_hand_thumb_1_joint` | -41.50 | 60.00 | 1.40 |
| `left_hand_thumb_2_joint` | 0.00 | 100.00 | 1.40 |
| `right_hand_index_0_joint` | 0.00 | 90.00 | 1.40 |
| `right_hand_middle_0_joint` | 0.00 | 90.00 | 1.40 |
| `right_hand_thumb_0_joint` | -60.00 | 60.00 | 2.45 |
| `right_hand_index_1_joint` | 0.00 | 100.00 | 1.40 |
| `right_hand_middle_1_joint` | 0.00 | 100.00 | 1.40 |
| `right_hand_thumb_1_joint` | -60.00 | 41.50 | 1.40 |
| `right_hand_thumb_2_joint` | -100.00 | 0.00 | 1.40 |
