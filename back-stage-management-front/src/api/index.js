/**
 * 所有的请求函数
 */
import ajax from "./ajax"
import base from "./base"
/**
 * 查询商品列表
 * params:{page:}
 */

export const getGoodsList=()=>ajax.get(base.goodslist,{params})