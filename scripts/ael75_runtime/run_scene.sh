#!/usr/bin/env bash
set -euo pipefail

mode=${1:-preview}
if (($#)); then shift; fi
case "$mode" in
    preview) view_args=(--visualizer kit --keep-open --view-only) ;;
    simulate) view_args=(--visualizer kit --keep-open) ;;
    headless) view_args=(--visualizer none) ;;
    *) echo 'Usage: run_scene.sh [preview|simulate|headless] [scene arguments...]' >&2; exit 2 ;;
esac

usd_utils=$(find /isaac-sim/extscache -path '*/bin/libusd_usdUtils.so' -print -quit)
physx_schema=$(find /isaac-sim/extscache -path '*/bin/libphysicsSchemaTools.so' -print -quit)
test -n "$usd_utils" && test -n "$physx_schema"

export LD_LIBRARY_PATH="$(dirname "$usd_utils"):$(dirname "$physx_schema"):${LD_LIBRARY_PATH:-}"
export PYTHONPATH="/workspaces/robot-move/scripts/ael75_runtime/pxr_preload${PYTHONPATH:+:$PYTHONPATH}"
export OMNI_KIT_ACCEPT_EULA=YES
export ACCEPT_EULA=Y

cd /workspaces/isaaclab_arena
exec ./submodules/IsaacLab/isaaclab.sh -p \
    /workspaces/robot-move/scripts/ael75_g1_box_scene.py \
    --steps 600 --physics isaacsim_physx "${view_args[@]}" "$@"
