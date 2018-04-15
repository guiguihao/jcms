import RequestType from './RequstType'
import RequstUser from './RequstUser'
import RequstArticle from './RequstArticle'
import Requestproduct from './Requestproduct'
import RequestproductSale from './RequestproductSale'
import RequstImg from './RequstImg'
import RequstReturnGoods from './RequstReturnGoods'
import RequestOrder from './RequestOrder'

var Request = {
	type:RequestType,
	user:RequstUser,
	article:RequstArticle,
	img:RequstImg,
	RequstReturnGoods:RequstReturnGoods,
	product:Requestproduct,
	productSale:RequestproductSale,
	order:RequestOrder,
};

export default Request