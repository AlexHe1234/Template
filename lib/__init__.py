import ipdb
from rich.traceback import *
from rich.console import Console, ConsoleOptions, RenderResult


def my_install(
    *,
    console: Optional[Console] = None,
    width: Optional[int] = 100,
    extra_lines: int = 3,
    theme: Optional[str] = None,
    word_wrap: bool = False,
    show_locals: bool = False,
    locals_max_length: int = LOCALS_MAX_LENGTH,
    locals_max_string: int = LOCALS_MAX_STRING,
    locals_hide_dunder: bool = True,
    locals_hide_sunder: Optional[bool] = None,
    indent_guides: bool = True,
    suppress: Iterable[Union[str, ModuleType]] = (),
    max_frames: int = 100,
) -> Callable[[Type[BaseException], BaseException, Optional[TracebackType]], Any]:
    """Install a rich traceback handler.

    Once installed, any tracebacks will be printed with syntax highlighting and rich formatting.


    Args:
        console (Optional[Console], optional): Console to write exception to. Default uses internal Console instance.
        width (Optional[int], optional): Width (in characters) of traceback. Defaults to 100.
        extra_lines (int, optional): Extra lines of code. Defaults to 3.
        theme (Optional[str], optional): Pygments theme to use in traceback. Defaults to ``None`` which will pick
            a theme appropriate for the platform.
        word_wrap (bool, optional): Enable word wrapping of long lines. Defaults to False.
        show_locals (bool, optional): Enable display of local variables. Defaults to False.
        locals_max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
            Defaults to 10.
        locals_max_string (int, optional): Maximum length of string before truncating, or None to disable. Defaults to 80.
        locals_hide_dunder (bool, optional): Hide locals prefixed with double underscore. Defaults to True.
        locals_hide_sunder (bool, optional): Hide locals prefixed with single underscore. Defaults to False.
        indent_guides (bool, optional): Enable indent guides in code and locals. Defaults to True.
        suppress (Sequence[Union[str, ModuleType]]): Optional sequence of modules or paths to exclude from traceback.

    Returns:
        Callable: The previous exception handler that was replaced.

    """
    traceback_console = Console(stderr=True) if console is None else console

    locals_hide_sunder = (
        True
        if (traceback_console.is_jupyter and locals_hide_sunder is None)
        else locals_hide_sunder
    )

    def excepthook(
        type_: Type[BaseException],
        value: BaseException,
        traceback: Optional[TracebackType],
    ) -> None:
        # display.deactivate()
        stack_info = Traceback.from_exception(
                type_,
                value,
                traceback,
                width=width,
                extra_lines=extra_lines,
                theme=theme,
                word_wrap=word_wrap,
                show_locals=show_locals,
                locals_max_length=locals_max_length,
                locals_max_string=locals_max_string,
                locals_hide_dunder=locals_hide_dunder,
                locals_hide_sunder=bool(locals_hide_sunder),
                indent_guides=indent_guides,
                suppress=suppress,
                max_frames=max_frames,
        )
        traceback_console.print(stack_info)
        # log.log(value, trace=False)
        ipdb.pm()

    def ipy_excepthook_closure(ip: Any) -> None:  # pragma: no cover
        tb_data = {}  # store information about showtraceback call
        default_showtraceback = ip.showtraceback  # keep reference of default traceback

        def ipy_show_traceback(*args: Any, **kwargs: Any) -> None:
            """wrap the default ip.showtraceback to store info for ip._showtraceback"""
            nonlocal tb_data
            tb_data = kwargs
            default_showtraceback(*args, **kwargs)

        def ipy_display_traceback(
            *args: Any, is_syntax: bool = False, **kwargs: Any
        ) -> None:
            """Internally called traceback from ip._showtraceback"""
            nonlocal tb_data
            exc_tuple = ip._get_exc_info()

            # do not display trace on syntax error
            tb: Optional[TracebackType] = None if is_syntax else exc_tuple[2]

            # determine correct tb_offset
            compiled = tb_data.get("running_compiled_code", False)
            tb_offset = tb_data.get("tb_offset", 1 if compiled else 0)
            # remove ipython internal frames from trace with tb_offset
            for _ in range(tb_offset):
                if tb is None:
                    break
                tb = tb.tb_next

            excepthook(exc_tuple[0], exc_tuple[1], tb)
            tb_data = {}  # clear data upon usage

        # replace _showtraceback instead of showtraceback to allow ipython features such as debugging to work
        # this is also what the ipython docs recommends to modify when subclassing InteractiveShell
        ip._showtraceback = ipy_display_traceback
        # add wrapper to capture tb_data
        ip.showtraceback = ipy_show_traceback
        ip.showsyntaxerror = lambda *args, **kwargs: ipy_display_traceback(
            *args, is_syntax=True, **kwargs
        )

    try:  # pragma: no cover
        # if within ipython, use customized traceback
        ip = get_ipython()  # type: ignore[name-defined]
        ipy_excepthook_closure(ip)
        return sys.excepthook
    except Exception:
        # otherwise use default system hook
        old_excepthook = sys.excepthook
        sys.excepthook = excepthook
        return old_excepthook


my_install()
