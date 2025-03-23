# https://wiki.nixos.org/wiki/Python

let
  # Check for new commits at https://status.nixos.org.
  commit = "7105ae3957700a9646cc4b766f5815b23ed0c682";
  tarbalUrl =  "https://github.com/NixOS/nixpkgs/archive/${commit}.tar.gz";
  pkgs = import (fetchTarball tarbalUrl) {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      pygame
      python-uinput
    ]))
  ];
}
