"""Launch a bounded G1 and small-box contact scene using Arena's robot asset."""

import argparse

BOX_SIZE_M = (0.09, 0.04, 0.06)
BOX_MASS_KG = 0.2
TABLE_SIZE_M = (0.65, 0.55, 0.04)
TABLE_TOP_Z_M = 0.76
BOX_FRICTION = (0.8, 0.6)
TABLE_FRICTION = (0.9, 0.7)


def box_diagonal_inertia_kg_m2() -> tuple[float, float, float]:
    """Return the solid cuboid inertia tensor diagonal for the configured box."""
    size_x, size_y, size_z = BOX_SIZE_M
    mass = BOX_MASS_KG
    return (
        mass * (size_y**2 + size_z**2) / 12.0,
        mass * (size_x**2 + size_z**2) / 12.0,
        mass * (size_x**2 + size_y**2) / 12.0,
    )


def sustained_contact_samples(
    contact_forces_n: list[float], minimum_force_n: float, window_steps: int
) -> tuple[int, int]:
    """Count above-threshold samples in a complete trailing contact window."""
    if window_steps < 1 or len(contact_forces_n) < window_steps:
        raise ValueError("A positive contact window must fit within the available force samples.")
    window = contact_forces_n[-window_steps:]
    return sum(force_n >= minimum_force_n for force_n in window), len(window)


def parse_args() -> argparse.Namespace:
    """Parse bounded rollout and simulator launcher arguments."""
    from isaaclab.app import add_launcher_args

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=600, help="Number of simulation steps (default: 600).")
    parser.add_argument("--log-interval", type=int, default=120, help="Contact log interval in steps.")
    parser.add_argument("--max-box-drift-m", type=float, default=0.005, help="Allowed box displacement in meters.")
    parser.add_argument(
        "--contact-window-steps",
        type=int,
        default=60,
        help="Trailing simulation steps used to check sustained table contact (default: 60).",
    )
    parser.add_argument(
        "--min-contact-fraction",
        type=float,
        default=0.9,
        help="Required fraction of the trailing window above the contact-force threshold (default: 0.9).",
    )
    parser.add_argument("--physics", default="isaacsim_physx", choices=["isaacsim_physx"])
    add_launcher_args(parser)
    args = parser.parse_args()
    if (
        args.steps < 1
        or args.log_interval < 1
        or args.max_box_drift_m <= 0
        or args.contact_window_steps < 1
        or args.contact_window_steps > args.steps
        or not 0.0 < args.min_contact_fraction <= 1.0
    ):
        parser.error(
            "steps, log interval, and contact window must be positive; contact window cannot exceed steps; "
            "box drift tolerance must be greater than zero; minimum contact fraction must be in (0, 1]."
        )
    return args


def main() -> None:
    """Simulate a standing G1 next to a box resting on a waist-height table."""
    args = parse_args()

    import isaaclab.sim as sim_utils
    from isaaclab.app import launch_simulation
    from isaaclab.assets import AssetBaseCfg, RigidObjectCfg
    from isaaclab.physics import PhysicsCfg
    from isaaclab.scene import InteractiveSceneCfg
    from isaaclab.sensors import ContactSensorCfg
    from isaaclab.sim.spawners.materials import UsdPhysicsRigidBodyMaterialCfg
    from isaaclab.utils import configclass, instantiate, replace
    from isaaclab.sim import SimulationContext
    from isaaclab_arena.embodiments.g1.g1 import G1_CFG

    robot_cfg = replace(
        G1_CFG,
        prim_path="{ENV_REGEX_NS}/Robot",
        init_state=replace(
            G1_CFG.init_state,
            pos=(0.0, 0.0, 0.78),
            rot=(0.0, 0.0, 0.0, 1.0),
        ),
    )

    @configclass
    class G1BoxSceneCfg(InteractiveSceneCfg):
        """One G1, a static table, a dynamic box, and a box contact sensor."""

        ground = AssetBaseCfg(prim_path="/World/ground", spawn=sim_utils.GroundPlaneCfg())
        light = AssetBaseCfg(
            prim_path="/World/Light",
            spawn=sim_utils.DomeLightCfg(intensity=2500.0, color=(0.8, 0.8, 0.8)),
        )
        robot = robot_cfg
        table = AssetBaseCfg(
            prim_path="{ENV_REGEX_NS}/Table",
            spawn=sim_utils.CuboidCfg(
                size=TABLE_SIZE_M,
                rigid_props=sim_utils.UsdPhysicsRigidBodyCfg(kinematic_enabled=True),
                collision_props=sim_utils.UsdPhysicsCollisionCfg(),
                physics_material=UsdPhysicsRigidBodyMaterialCfg(
                    static_friction=TABLE_FRICTION[0],
                    dynamic_friction=TABLE_FRICTION[1],
                    restitution=0.0,
                ),
                visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.28, 0.31, 0.34)),
                activate_contact_sensors=True,
            ),
            init_state=AssetBaseCfg.InitialStateCfg(pos=(0.48, 0.0, TABLE_TOP_Z_M - TABLE_SIZE_M[2] / 2.0)),
        )
        box = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Box",
            spawn=sim_utils.CuboidCfg(
                size=BOX_SIZE_M,
                rigid_props=sim_utils.UsdPhysicsRigidBodyCfg(),
                mass_props=sim_utils.MassCfg(mass=BOX_MASS_KG),
                collision_props=sim_utils.UsdPhysicsCollisionCfg(),
                physics_material=UsdPhysicsRigidBodyMaterialCfg(
                    static_friction=BOX_FRICTION[0],
                    dynamic_friction=BOX_FRICTION[1],
                    restitution=0.0,
                ),
                visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.68, 0.38, 0.18)),
                activate_contact_sensors=True,
            ),
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=(0.48, 0.0, TABLE_TOP_Z_M + BOX_SIZE_M[2] / 2.0),
            ),
        )
        box_contact = ContactSensorCfg(
            prim_path="{ENV_REGEX_NS}/Box",
            update_period=0.0,
            history_length=1,
            debug_vis=True,
            filter_prim_paths_expr=["{ENV_REGEX_NS}/Table"],
        )

    with launch_simulation(cfg=PhysicsCfg(), launcher_args=args) as physics_cfg:
        from pxr import Gf, UsdPhysics

        sim_cfg = sim_utils.SimulationCfg(dt=1.0 / 120.0, device=args.device, physics=physics_cfg)
        sim = SimulationContext(sim_cfg)
        sim.set_camera_view(eye=(1.55, 1.75, 1.35), target=(0.38, 0.0, 0.82))
        scene = instantiate(G1BoxSceneCfg(num_envs=1, env_spacing=2.0))

        box_prim = sim.stage.GetPrimAtPath("/World/envs/env_0/Box")
        assert box_prim.IsValid(), "The configured box prim was not spawned."
        mass_api = UsdPhysics.MassAPI.Apply(box_prim)
        mass_api.GetMassAttr().Set(BOX_MASS_KG)
        mass_api.GetDiagonalInertiaAttr().Set(Gf.Vec3f(*box_diagonal_inertia_kg_m2()))
        mass_api.GetPrincipalAxesAttr().Set(Gf.Quatf(1.0, Gf.Vec3f(0.0, 0.0, 0.0)))

        sim.reset()
        scene.reset()
        robot = scene["robot"]
        box = scene["box"]
        robot.actuators.target_command.set_position_index(value=robot.data.default_joint_pos.torch)
        initial_box_pos_w = box.data.root_pos_w.torch[0].clone()

        print(f"[AEL-75] robot_usd={robot_cfg.spawn.usd_path}")
        print(f"[AEL-75] robot_joints={robot.num_joints}")
        hand_joint_names = [name for name in robot.data.joint_names if "hand" in name]
        print(f"[AEL-75] hand_joints={len(hand_joint_names)} names={hand_joint_names}")
        print(f"[AEL-75] box_size_m={BOX_SIZE_M} box_mass_kg={BOX_MASS_KG}")
        print(f"[AEL-75] box_inertia_kg_m2={box_diagonal_inertia_kg_m2()}")
        print(f"[AEL-75] box_friction_static_dynamic={BOX_FRICTION}")

        minimum_table_contact_n = BOX_MASS_KG * 9.81 * 0.5
        table_contact_forces_n = []
        for step in range(1, args.steps + 1):
            scene.write_data_to_sim()
            sim.step()
            scene.update(sim_cfg.dt)
            table_normal_force_matrix_w = scene["box_contact"].data.normal_force_matrix_w
            if table_normal_force_matrix_w is None:
                raise RuntimeError("The box contact sensor did not report table-filtered normal forces.")
            table_contact_force_n = table_normal_force_matrix_w.torch.norm(dim=-1).max().item()
            table_contact_forces_n.append(table_contact_force_n)
            if step % args.log_interval == 0 or step == args.steps:
                print(f"[AEL-75] step={step} box_table_normal_force_n={table_contact_force_n:.3f}")

        sustained_contact_count, sustained_contact_window_size = sustained_contact_samples(
            table_contact_forces_n,
            minimum_table_contact_n,
            args.contact_window_steps,
        )
        sustained_contact_fraction = sustained_contact_count / sustained_contact_window_size
        print(
            f"[AEL-75] trailing_contact_window_steps={args.contact_window_steps} "
            f"contact_samples={sustained_contact_count}/{sustained_contact_window_size} "
            f"contact_fraction={sustained_contact_fraction:.3f} "
            f"required_fraction={args.min_contact_fraction:.3f}"
        )

        final_box_pos_w = box.data.root_pos_w.torch[0]
        box_drift_m = (final_box_pos_w - initial_box_pos_w).norm().item()
        print(f"[AEL-75] box_drift_m={box_drift_m:.6f}")
        if robot.num_joints != 43:
            raise RuntimeError(f"Expected G1 29-DoF + Dex3 14-DoF (43 joints), got {robot.num_joints}.")
        if len(hand_joint_names) != 14:
            raise RuntimeError(f"Expected 14 Dex3 hand joints, got {len(hand_joint_names)}.")
        for hand_side in ("left", "right"):
            side_joint_count = sum(name.startswith(f"{hand_side}_hand_") for name in hand_joint_names)
            if side_joint_count != 7:
                raise RuntimeError(f"Expected 7 {hand_side} Dex3 joints, got {side_joint_count}.")
        if box_drift_m > args.max_box_drift_m:
            raise RuntimeError(
                f"The box moved {box_drift_m:.6f} m; allowed drift is {args.max_box_drift_m:.6f} m."
            )
        if sustained_contact_fraction < args.min_contact_fraction:
            raise RuntimeError(
                f"Box/table contact exceeded {minimum_table_contact_n:.3f} N in "
                f"{sustained_contact_count}/{sustained_contact_window_size} trailing samples "
                f"({sustained_contact_fraction:.3f}); required fraction is {args.min_contact_fraction:.3f}."
            )


if __name__ == "__main__":
    main()
