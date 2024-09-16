# Sao kê từ góc nhìn phân tích dự liệu lớn

Hơn 10 nghìn trang PDF dữ liệu là một khối dữ liệu tương đối lớn mà không phải lúc nào cũng có thể dễ dàng có được, vì thế ngoài góc nhìn về việc check var như trên mạng mấy ngày gần đây, thì đối với dân data analysis mà nói đây như một kho vàng để thực hành phân tích dữ liệu.

Với data ngày thì có thể làm được gì?
- Phân tích số lượng tiền đóng góp, tổng số, phân bổ theo thời gian, phân bổ theo giá trị.
- Phân tích nội dung chuyển khoản, xu hướng nội dung, phân tích từ khóa.

Các bước thực hiện:
1. Từ file PDF có được, truy xuất dữ liệu ra thành excel hoặc database.
- Khuyên khích phân tích thành excel trước, để tiền kiểm dữ liệu, cũng như giảm thời gian xử lý sau này.
- Import dữ liệu từ excel vào database để dễ dàng tìm kiếm, phân tích.

2. Phân tích và thống kê:
- Thông kê tổng số tiền.
- Thống kê số giao dịch, số tiền theo ngày.
- Phân tích tỉ trọng số tiền theo nhóm < 50k, < 100k, ... (Nếu nhóm có dữ liệu lớn thì tiếp tục chi nhỏ).
- Phân tích nội dung chuyển khoản, nhóm các từ khóa để phân tích xu hướng nội dung chuyển khoản.