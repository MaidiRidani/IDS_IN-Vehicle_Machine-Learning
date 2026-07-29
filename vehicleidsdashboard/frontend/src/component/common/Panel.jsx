function Panel({
    children,
    className = "",
    border = true,
    background = "#101B30",
    style = {},
}) {
    return (
        <div
            className={`
                rounded-xl
                ${border ? "border border-[#243552]" : ""}
                ${className}
            `}
            style={{
                backgroundColor: background,
                ...style,
            }}
        >
            {children}
        </div>
    );
}

export default Panel;