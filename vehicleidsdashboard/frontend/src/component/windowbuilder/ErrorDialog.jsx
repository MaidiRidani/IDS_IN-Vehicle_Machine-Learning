import Panel from "../common/Panel";

function ErrorDialog({
    show,
    title = "Configuration Failed",
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
                w-[340px]
                h-[180px]
                z-[100]
            "
            background="#17233A"
        >

            <div className="relative w-full h-full">

                <h2
                    className="
                        absolute
                        left-0
                        top-[18px]
                        w-full
                        text-center
                        text-[18px]
                        font-bold
                    "
                >
                    {title}
                </h2>

                <p
                    className="
                        absolute
                        left-[24px]
                        right-[24px]
                        top-[58px]
                        text-center
                        text-[13px]
                        leading-5
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
                        w-[90px]
                        h-[30px]
                        rounded-full
                        bg-[#13832F]
                        text-[12px]
                        font-bold
                    "
                    onClick={onClose}
                >
                    OK
                </button>

            </div>

        </Panel>

    );

}

export default ErrorDialog;