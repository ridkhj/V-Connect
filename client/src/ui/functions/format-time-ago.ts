function formatTimeAgo(date: Date) {
    const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);

    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + 'y atrás';

    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + 'm atrás';

    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + 'd atrás';

    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + 'h atrás';

    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + 'm atrás';

    return Math.floor(seconds) + 's atrás';
};

export default formatTimeAgo;