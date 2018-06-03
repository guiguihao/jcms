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
import RequestSiteinfo from './RequestSiteinfo'
import RequestFenXiao from './RequestFenXiao'
import RequestImg2 from './RequestImg2'
import RequestAds from './RequestAds'
import RequestCollection from './RequestCollection'
import RequestReceiveInfo from './RequestReceiveInfo'

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
	siteInfo:RequestSiteinfo,
	fenxiao:RequestFenXiao,
	img2:RequestImg2,
	ad:RequestAds,
	collection:RequestCollection,
	receiveInfo:RequestReceiveInfo,
};

export default Request