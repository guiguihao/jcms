import RequestType from './RequstType'
import RequstUser from './RequstUser'
import RequstArticle from './RequstArticle'
import Requestproduct from './Requestproduct'
import RequestproductSale from './RequestproductSale'
import RequestProductSaleCode from './RequestProductSaleCode'
import RequstImg from './RequstImg'
import RequstReturnGoods from './RequstReturnGoods'
import RequestOrder from './RequestOrder'
import RequestComment from './RequestComment'

var Request = {
	type:RequestType,
	user:RequstUser,
	article:RequstArticle,
	img:RequstImg,
	RequstReturnGoods:RequstReturnGoods,
	product:Requestproduct,
	productSale:RequestproductSale,
	ProductSaleCode:RequestProductSaleCode,
	order:RequestOrder,
	comment:RequestComment,
};

export default Request