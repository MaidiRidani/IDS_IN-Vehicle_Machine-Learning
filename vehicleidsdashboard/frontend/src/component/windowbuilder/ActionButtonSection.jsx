function ActionButtonSection({

    setShow,
    canSave,

    onSave,

    onClearConfigurations,

    onRandom,

}) {
    return (

        <>

            {/* ================= CLEAR ================= */}

            <button
                className="
                    absolute
                    w-[66px]
                    h-[18px]
                    rounded-full
                    bg-[#831315]
                    text-[10px]
                    font-bold
                "
                style={{
                    left: "265px",
                    top: "22px",
                }}
                onClick={onClearConfigurations}
            >
                CLEAR
            </button>

            {/* ================= Random ================= */}

            <button
                className="
                    absolute
                    w-[66px]
                    h-[18px]
                    rounded-full
                    bg-[#831315]
                    text-[12px]
                    font-bold
                "
                style={{
                    left: "348px",
                    top: "22px",
                }}
                onClick={onRandom}
            >
                Random
            </button>


            {/* ================= SAVE ================= */}

            <button
                disabled={!canSave}
                className={`
                    absolute
                    w-[66px]
                    h-[18px]
                    rounded-full
                    bg-[#13832F]
                    text-[12px]
                    font-bold
                    ${
                        canSave

                            ? "bg-[#13832F]"

                            : "bg-[#778795] cursor-not-allowed"

                    }
                `}
                style={{
                    left: "430px",
                    top: "22px",
                }}
                onClick={onSave}
            >
                SAVE
            </button>

            {/* ================= EXIT ================= */}

            <button
                className="
                    absolute
                    w-[66px]
                    h-[18px]
                    rounded-full
                    bg-[#831315]
                    text-[12px]
                    font-bold
                "
                style={{
                    left: "509px",
                    top: "22px",
                }}
                onClick={() => setShow(false)}
            >
                EXIT
            </button>

        </>

    );
}

export default ActionButtonSection;