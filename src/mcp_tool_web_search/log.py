"""日志配置。"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def setup_logging(
    log_dir: str = "",
    console: bool = True,
    level: int = logging.INFO,
) -> None:
    """配置全局日志。

    Args:
        log_dir: 日志目录，为空则不输出到文件。
            文件名按启动时间自动生成，如 ``20260223_214530.log``。
        console: 是否输出到终端。
        level: 日志级别。
    """
    handlers: list[logging.Handler] = []

    if console:
        sh = logging.StreamHandler(sys.stderr)
        sh.setFormatter(logging.Formatter(_FMT))
        handlers.append(sh)

    if log_dir:
        dirpath = Path(log_dir)
        dirpath.mkdir(parents=True, exist_ok=True)
        filename = datetime.now().strftime("%Y%m%d_%H%M%S.log")
        fh = logging.FileHandler(str(dirpath / filename), encoding="utf-8")
        fh.setFormatter(logging.Formatter(_FMT))
        handlers.append(fh)

    logging.basicConfig(level=level, handlers=handlers, force=True)
