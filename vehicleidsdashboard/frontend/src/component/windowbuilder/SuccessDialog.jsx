import Panel from "../common/Panel";

function SuccessDialog({
    show,
    message,
    onClose,
}) {

    if (!show) {

        return null;

    }

    return (

        <Panel
            className="
                absolute
                left-1/2
                top-1/2
                -translate-x-1/2
                -translate-y-1/2
                w-[330px]
                h-[180px]
                z-[100]
            "
        >

            <h2
                className="
                    text-center
                    text-[18px]
                    font-bold
                    mt-[20px]
                "
            >
                Configuration Saved
            </h2>

            <p
                className="
                    text-center
                    text-[14px]
                    mt-[28px]
                    px-[20px]
                "
            >
                {message}
            </p>

            <button
                className="
                    absolute
                    left-1/2
                    -translate-x-1/2
                    bottom-[18px]
                    w-[110px]
                    h-[32px]
                    rounded-full
                    bg-[#13832F]
                    text-[14px]
                    font-bold
                "
                onClick={onClose}
            >
                OK
            </button>

        </Panel>

    );

}

export default SuccessDialog;