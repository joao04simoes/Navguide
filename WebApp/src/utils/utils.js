export function NextHeading(atualPosition, NextPosition) {
    let NextHeading = 0
    if (atualPosition[0] === NextPosition[0] && atualPosition[1] > NextPosition[1])
        NextHeading = 3
    else if (atualPosition[0] === NextPosition[0] && atualPosition[1] < NextPosition[1])
        NextHeading = 1
    else if (atualPosition[0] > NextPosition[0] && atualPosition[1] === NextPosition[1])
        NextHeading = 4
    else if (atualPosition[0] < NextPosition[0] && atualPosition[1] === NextPosition[1])
        NextHeading = 2
    return NextHeading
}

export function GiveDirection(atualHeading, NextHeading) {
    const diff = atualHeading - NextHeading
    if (atualHeading === NextHeading)
        return "forward"
    else if (Math.abs(diff) === 2)
        return "backward"
    else if (diff === 1 || diff === -3)
        return "left"
    else if (diff === -1 || diff === 3)
        return "right"
    else
        return "error"

}
