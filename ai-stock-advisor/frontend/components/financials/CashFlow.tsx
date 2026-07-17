"use client";

interface Props {
    data: Record<string, number | null>;
}

function formatValue(value: number | null) {

    if (value === null || value === undefined)
        return "-";

    if (Math.abs(value) >= 1_000_000_000)
        return `$${(value / 1_000_000_000).toFixed(2)}B`;

    if (Math.abs(value) >= 1_000_000)
        return `$${(value / 1_000_000).toFixed(2)}M`;

    return value.toLocaleString();
}

export default function CashFlow({
    data,
}: Props) {

    return (

        <table className="w-full">

            <tbody>

                {

                    Object.entries(data).map(

                        ([key, value]) => (

                            <tr
                                key={key}
                                className="border-b"
                            >

                                <td className="py-3 font-medium">

                                    {key
                                        .replaceAll("_", " ")
                                        .replace(/\b\w/g, c =>
                                            c.toUpperCase()
                                        )}

                                </td>

                                <td className="py-3 text-right">

                                    {formatValue(value)}

                                </td>

                            </tr>

                        )

                    )

                }

            </tbody>

        </table>

    );

}