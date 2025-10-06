export const TimeFormatter = {
  /**
   * 解析时间输入，统一为 Date 对象
   * @param {Date | number | string} input
   * @returns {Date}
   */
  parse(input) {
    if (input instanceof Date) return input;
    if (typeof input === 'number') return new Date(input);
    if (typeof input === 'string') {
      const parsed = new Date(input);
      if (!isNaN(parsed.getTime())) return parsed;
    }
    throw new Error('Invalid time input');
  },

  /**
   * 补零
   */
  pad(n) {
    return n.toString().padStart(2, '0');
  },

  /**
   * 格式化为 yyyy-MM-dd HH:mm:ss（默认使用本地时间）
   * @param {Date | number | string} input
   * @param {Object} options
   * @param {boolean} options.useUTC 是否使用 UTC 展示
   */
  formatFull(input, { useUTC = false } = {}) {
    const date = TimeFormatter.parse(input);
    const get = useUTC ? {
      year: date.getUTCFullYear(),
      month: date.getUTCMonth() + 1,
      day: date.getUTCDate(),
      hour: date.getUTCHours(),
      minute: date.getUTCMinutes(),
      second: date.getUTCSeconds()
    } : {
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      day: date.getDate(),
      hour: date.getHours(),
      minute: date.getMinutes(),
      second: date.getSeconds()
    };

    return `${get.year}-${TimeFormatter.pad(get.month)}-${TimeFormatter.pad(get.day)} ${TimeFormatter.pad(get.hour)}:${TimeFormatter.pad(get.minute)}:${TimeFormatter.pad(get.second)}`;
  },

  formatDate(input, { useUTC = false } = {}) {
    const date = TimeFormatter.parse(input);
    const get = useUTC ? {
      year: date.getUTCFullYear(),
      month: date.getUTCMonth() + 1,
      day: date.getUTCDate()
    } : {
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      day: date.getDate()
    };

    return `${get.year}-${TimeFormatter.pad(get.month)}-${TimeFormatter.pad(get.day)}`;
  },

  formatTime(input, { useUTC = false } = {}) {
    const date = TimeFormatter.parse(input);
    const get = useUTC ? {
      hour: date.getUTCHours(),
      minute: date.getUTCMinutes(),
      second: date.getUTCSeconds()
    } : {
      hour: date.getHours(),
      minute: date.getMinutes(),
      second: date.getSeconds()
    };

    return `${TimeFormatter.pad(get.hour)}:${TimeFormatter.pad(get.minute)}:${TimeFormatter.pad(get.second)}`;
  },

  formatRelative(input) {
    const date = TimeFormatter.parse(input);
    const now = Date.now();
    const time = date.getTime();
    const diff = Math.floor((now - time) / 1000);
    if (diff < 60) return `${diff}秒前`;
    if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`;
    if (diff < 2592000) return `${Math.floor(diff / 86400)}天前`;
    return TimeFormatter.formatDate(input);
  }
};
